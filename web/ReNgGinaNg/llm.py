
import logging
import openai
import re
from ReNgGinaNg.common_func import get_open_ai_key, parse_llm_vulnerability_report
from ReNgGinaNg.definitions import (
	VULNERABILITY_DESCRIPTION_SYSTEM_MESSAGE,
	ATTACK_SUGGESTION_GPT_SYSTEM_PROMPT,
	OLLAMA_INSTANCE,
	INDONESIAN_LANGUAGE_INSTRUCTION,
	REPORT_ENRICHMENT_SYSTEM_PROMPT,
	EXECUTIVE_REMEDIATION_SYSTEM_PROMPT,
)
from langchain_community.llms import Ollama

from dashboard.models import OllamaSettings

logger = logging.getLogger(__name__)


class LLMVulnerabilityReportGenerator:

	def __init__(self, logger):
		selected_model = OllamaSettings.objects.first()
		self.model_name = selected_model.selected_model if selected_model else 'gpt-3.5-turbo'
		self.use_ollama = selected_model.use_ollama if selected_model else False
		self.openai_api_key = None
		self.logger = logger

	def get_vulnerability_description(self, description):
		"""Generate Vulnerability Description using GPT.

		Args:
			description (str): Vulnerability Description message to pass to GPT.

		Returns:
			(dict) of {
				'description': (str)
				'impact': (str),
				'remediation': (str),
				'references': (list) of urls
			}
		"""
		self.logger.info(f"Generating Vulnerability Description for: {description}")
		if self.use_ollama:
			prompt = VULNERABILITY_DESCRIPTION_SYSTEM_MESSAGE + "\nUser: " + description
			prompt = re.sub(r'\t', '', prompt)
			self.logger.info(f"Using Ollama for Vulnerability Description Generation")
			llm = Ollama(
				base_url=OLLAMA_INSTANCE,
				model=self.model_name
			)
			response_content = llm.invoke(prompt)
			# self.logger.info(response_content)
		else:
			self.logger.info(f'Using OpenAI API for Vulnerability Description Generation')
			openai_api_key = get_open_ai_key()
			if not openai_api_key:
				return {
					'status': False,
					'error': 'OpenAI API Key not set'
				}
			try:
				prompt = re.sub(r'\t', '', VULNERABILITY_DESCRIPTION_SYSTEM_MESSAGE)
				openai.api_key = openai_api_key
				gpt_response = openai.ChatCompletion.create(
				model=self.model_name,
				messages=[
						{'role': 'system', 'content': prompt},
						{'role': 'user', 'content': description}
					]
				)

				response_content = gpt_response['choices'][0]['message']['content']
			except Exception as e:
				return {
					'status': False,
					'error': str(e)
				}

		response = parse_llm_vulnerability_report(response_content)

		if not response:
			return {
				'status': False,
				'error': 'Failed to parse LLM response'
			}

		return {
			'status': True,
			'description': response.get('description', ''),
			'impact': response.get('impact', ''),
			'remediation': response.get('remediation', ''),
			'references': response.get('references', []),
		}


class LLMAttackSuggestionGenerator:

	def __init__(self, logger):
		selected_model = OllamaSettings.objects.first()
		self.model_name = selected_model.selected_model if selected_model else 'gpt-3.5-turbo'
		self.use_ollama = selected_model.use_ollama if selected_model else False
		self.openai_api_key = None
		self.logger = logger

	def get_attack_suggestion(self, user_input):
		'''
			user_input (str): input for gpt
		'''
		if self.use_ollama:
			self.logger.info(f"Using Ollama for Attack Suggestion Generation")
			prompt = ATTACK_SUGGESTION_GPT_SYSTEM_PROMPT + "\nUser: " + user_input
			prompt = re.sub(r'\t', '', prompt)
			llm = Ollama(
				base_url=OLLAMA_INSTANCE,
				model=self.model_name
			)
			response_content = llm.invoke(prompt)
			self.logger.info(response_content)
		else:
			self.logger.info(f'Using OpenAI API for Attack Suggestion Generation')
			openai_api_key = get_open_ai_key()
			if not openai_api_key:
				return {
					'status': False,
					'error': 'OpenAI API Key not set'
				}
			try:
				prompt = re.sub(r'\t', '', ATTACK_SUGGESTION_GPT_SYSTEM_PROMPT)
				openai.api_key = openai_api_key
				gpt_response = openai.ChatCompletion.create(
				model=self.model_name,
				messages=[
						{'role': 'system', 'content': prompt},
						{'role': 'user', 'content': user_input}
					]
				)
				response_content = gpt_response['choices'][0]['message']['content']
			except Exception as e:
				return {
					'status': False,
					'error': str(e),
					'input': user_input
				}
		return {
			'status': True,
			'description': response_content,
			'input': user_input
		}


class LLMReportEnricher:

	def __init__(self, language='en'):
		selected_model = OllamaSettings.objects.first()
		self.model_name = selected_model.selected_model if selected_model else 'gpt-3.5-turbo'
		self.use_ollama = selected_model.use_ollama if selected_model else False
		self.language = language

	def _get_language_instruction(self):
		if self.language == 'id':
			return INDONESIAN_LANGUAGE_INSTRUCTION
		return ''

	def _call_llm(self, system_prompt, user_message):
		lang_instruction = self._get_language_instruction()
		full_system_prompt = re.sub(r'\t', '', system_prompt + lang_instruction)

		if self.use_ollama:
			prompt = full_system_prompt + "\nUser: " + user_message
			llm = Ollama(
				base_url=OLLAMA_INSTANCE,
				model=self.model_name
			)
			return llm.invoke(prompt)
		else:
			openai_api_key = get_open_ai_key()
			if not openai_api_key:
				return None
			try:
				openai.api_key = openai_api_key
				gpt_response = openai.ChatCompletion.create(
					model=self.model_name,
					messages=[
						{'role': 'system', 'content': full_system_prompt},
						{'role': 'user', 'content': user_message}
					]
				)
				return gpt_response['choices'][0]['message']['content']
			except Exception as e:
				logger.error(f"LLM API error: {e}")
				return None

	def enrich_vulnerability(self, vuln):
		from startScan.models import GPTVulnerabilityReport, VulnerabilityReference

		if vuln.remediation and vuln.impact:
			return

		# Check GPTVulnerabilityReport cache
		cached = GPTVulnerabilityReport.objects.filter(title=vuln.name).first()
		if cached:
			if not vuln.remediation and cached.remediation:
				vuln.remediation = cached.remediation
			if not vuln.impact and cached.impact:
				vuln.impact = cached.impact
			if not vuln.description and cached.description:
				vuln.description = cached.description
			vuln.save()
			if vuln.remediation and vuln.impact:
				return

		# Call LLM for missing fields
		user_message = f"Vulnerability: {vuln.name}\n"
		if vuln.description:
			user_message += f"Description: {vuln.description}\n"
		if vuln.http_url:
			user_message += f"URL: {vuln.http_url}\n"

		response_content = self._call_llm(REPORT_ENRICHMENT_SYSTEM_PROMPT, user_message)
		if not response_content:
			return

		parsed = parse_llm_vulnerability_report(response_content)
		if not parsed:
			return

		# Update vulnerability with missing fields
		if not vuln.remediation and parsed.get('remediation'):
			vuln.remediation = parsed['remediation']
		if not vuln.impact and parsed.get('impact'):
			vuln.impact = parsed['impact']
		if not vuln.description and parsed.get('description'):
			vuln.description = parsed['description']
		vuln.save()

		# Add references if any
		for ref_url in parsed.get('references', []):
			ref_url = ref_url.lstrip('- ').strip()
			if ref_url.startswith(('http://', 'https://')):
				ref_obj, _ = VulnerabilityReference.objects.get_or_create(url=ref_url)
				vuln.references.add(ref_obj)

		# Update or create cache entry
		cache_obj, created = GPTVulnerabilityReport.objects.get_or_create(
			title=vuln.name,
			defaults={
				'url_path': vuln.http_url or '',
				'description': parsed.get('description', ''),
				'impact': parsed.get('impact', ''),
				'remediation': parsed.get('remediation', ''),
			}
		)
		if not created:
			if parsed.get('description') and not cache_obj.description:
				cache_obj.description = parsed['description']
			if parsed.get('impact') and not cache_obj.impact:
				cache_obj.impact = parsed['impact']
			if parsed.get('remediation') and not cache_obj.remediation:
				cache_obj.remediation = parsed['remediation']
			cache_obj.save()

	def generate_executive_summary_remediation(self, vulnerabilities):
		medium_and_above = vulnerabilities.filter(severity__gte=2).order_by('-severity')[:20]
		if not medium_and_above.exists():
			return None

		vuln_list = []
		for v in medium_and_above:
			severity_map = {4: 'Critical', 3: 'High', 2: 'Medium'}
			sev = severity_map.get(v.severity, 'Medium')
			vuln_list.append(f"- [{sev}] {v.name}")

		user_message = "Vulnerabilities found during the assessment:\n" + "\n".join(vuln_list)

		if self.language == 'id':
			user_message += "\n\nWrite the remediation plan in Indonesian (Bahasa Indonesia). Keep section headers in English for consistency."

		return self._call_llm(EXECUTIVE_REMEDIATION_SYSTEM_PROMPT, user_message)
