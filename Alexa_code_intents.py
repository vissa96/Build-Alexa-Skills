
import random
import logging
import requests
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.advisor import AdvisorManagementClient
import json
import datetime as dt

SKILL_NAME = "Space Facts"
GET_FACT_MESSAGE = "Here's your fact: "
HELP_MESSAGE = "You can say tell me a space fact, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "Sorry, I couldn't help you with that. "
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."



sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HelloIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("HelloIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In hellointent")
        actiontype = "hello"


        speech = "Welcome to our skill, Powered by Prashant Vissa "

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, actiontype))
        return handler_input.response_builder.set_should_end_session(False).response



class GetsecurityIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch and security recommendations from azure"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetsecurityIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In getsecurityintent")
        actiontype = "security"
        credentials = ServicePrincipalCredentials(client_id='xxx',secret='xxx',tenant='xxx')
        subscription_id = 'xxx'
        advisorClient = AdvisorManagementClient(credentials, subscription_id)
        vm = []
        desc = []
        count = 0
        for recommendation in advisorClient.recommendations.list():

            if recommendation.category == "Security":
                count = count + 1
                desc.append(recommendation.short_description.problem)
                vm.append(recommendation.impacted_value)


        speech = "You have " + str(count) + " security recommendations from Azure. They are , "
        for x in range(0,count):
            speech = speech + ". For the machine " + vm[x] + " , " + desc[x] +"."
        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, actiontype))
        return handler_input.response_builder.set_should_end_session(False).response


# Built-in VMIntent Handlers
class GetVMIntentHandler(AbstractRequestHandler):
    """Handler for Skill Launch and get VM information from azure."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetVMIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In getvmintent")
        actiontype = "VM"
        credentials = ServicePrincipalCredentials(client_id='xxx',secret='xxx',tenant='xxx')
        subscription_id = 'xxx'
        compute_client = ComputeManagementClient(credentials, subscription_id)

        resource_client = ResourceManagementClient(credentials, subscription_id)
        resource_group_name = 'xxx'
        on_machines = []
        count = 0
        oncount = 0
        for vm_size in compute_client.virtual_machines.list(resource_group_name):
            status = compute_client.virtual_machines.get(resource_group_name, vm_size.name, expand='instanceView').instance_view.statuses[1].display_status
            count = count + 1
            if status == "VM running" or status == "VM starting":
                oncount = oncount + 1
                on_machines.append(str(vm_size.name))
        

        speech = " You have " + str(oncount) + " virtual machines running out of " + str(count) + " virtual machines. "
        if oncount > 0:
            speech = speech + "In the current resource group , the virtual machines running are "

            for item in on_machines:
                speech = speech + str(item) + ","

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, actiontype))
        return handler_input.response_builder.set_should_end_session(False).response





class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers

sb.add_request_handler(HelloIntentHandler())
sb.add_request_handler(GetsecurityIntentHandler())
sb.add_request_handler(GetVMIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
