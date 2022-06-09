"""
    Open Assessment Template mixin helps out in generating different presets to display in studio.
"""

from django.utils.translation import gettext as _

from openassessment.xblock.defaults import (BLANK_ASSESSMENT_MODULES, PEER_ASSESSMENT_MODULES, SELF_ASSESSMENT_MODULES,
                                            SELF_TO_PEER_ASSESSMENT_MODULES, SELF_TO_STAFF_ASSESSMENT_MODULES,
                                            STAFF_ASSESSMENT_MODULES)


class OpenAssessmentTemplatesMixin:
    """
    This helps to get templates for different type of assessment that is
    offered.
    """

    VALID_ASSESSMENT_TYPES_DISPLAY_NAMES = {
        "peer-assessment": _("Peer Assessment Only"),
        "self-assessment": _("Self Assessment Only"),
        "staff-assessment": _("Staff Assessment Only"),
        "self-to-peer": _("Self Assessment to Peer Assessment"),
        "self-to-staff": _("Self Assessment to Staff Assessment")
    }

    VALID_ASSESSMENT_TYPES_ASSESSMENT_MODULE = {
        "self-assessment": SELF_ASSESSMENT_MODULES,
        "peer-assessment": PEER_ASSESSMENT_MODULES,
        "staff-assessment": STAFF_ASSESSMENT_MODULES,
        "self-to-peer": SELF_TO_PEER_ASSESSMENT_MODULES,
        "self-to-staff": SELF_TO_STAFF_ASSESSMENT_MODULES,
        "blank-assessment": BLANK_ASSESSMENT_MODULES
    }

    @classmethod
    def templates(cls):
        """
        Returns a list of dictionary field: value objects that describe possible templates.
        """
        templates = []
        for assesment_type, display_name in cls.VALID_ASSESSMENT_TYPES_DISPLAY_NAMES.items():
            template_id = assesment_type
            template = cls._create_template_dict(template_id, display_name)
            templates.append(template)
        templates.append({
            'template_id': 'ora-without-criterions',
            'metadata': {'display_name': 'Open Response Assessment without Criterions'}
        })
        templates.append({
            'template_id': 'ora-additional-rubric',
            'metadata': {'display_name': 'Open Response Assessment: Additional Rubric'}
        })
        return templates

    @classmethod
    def _create_template_dict(cls, template_id, display_name):
        """
        Creates a dictionary for serving various metadata for the template.

        Args:
            template_id(str): template id of what assessement template needs to be served.
            display_name(str): display name of template.

        Returns:
            A dictionary with proper keys to be consumed.
        """
        return {
            "template_id": template_id,
            "metadata": {
                "display_name": display_name,
            }
        }

    @classmethod
    def get_template(cls, template_id):
        """
        Helps to generate various option level template for ORA.

        Args:
            template_id(str): template id of what assessement template needs to be served.

        Returns:
            A dictionary of payload to be consumed by Studio.
        """
        if template_id == 'ora-additional-rubric':
            return {
                'metadata': {
                    'display_name': 'Additional Rubric',
                    'title': 'Additional Rubric',
                    'is_additional_rubric': True,
                    'prompt': '',
                    'prompts_type': 'html',
                    'rubric_assessments': [
                        {
                            'must_grade': 5,
                            'name': 'peer-assessment',
                            'must_be_graded_by': 3,
                            'start': '2001-01-01T00:00:00+00:00',
                            'due': '2029-01-01T00:00:00+00:00'
                        }, {
                            'name': 'self-assessment',
                            'start': '2001-01-01T00:00:00+00:00',
                            'due': '2029-01-01T00:00:00+00:00'
                        }, {
                            'name': 'staff-assessment',
                            'start': None,
                            'due': None,
                            'required': True
                        }]
                },
                'data': {

                }
            }
        elif template_id == 'ora-without-criterions':
            return {
                'metadata': {
                    'display_name': 'Open Response Assessment',
                    'title': 'Open Response Assessment',
                    'rubric_criteria': [],
                    'rubric_assessments': [{
                        'name': 'staff-assessment',
                        'start': None,
                        'due': None,
                        'required': True
                    }]
                },
                'data': {

                }
            }

        rubric_assessments = cls._create_rubric_assessment_dict(template_id)
        return {
            "data": rubric_assessments
        }

    @classmethod
    def _create_rubric_assessment_dict(cls, template_id):
        """
        Creates a dictionary of parameters to be passed while creating ORA xblock.

        Args:
            template_id(str): template id of what assessement template needs to be served.

        Returns:
            A dictionary of payload to be consumed by Studio.
        """
        assessment_module = cls.VALID_ASSESSMENT_TYPES_ASSESSMENT_MODULE \
            .get(template_id)
        return {
            "rubric_assessments": assessment_module
        }
