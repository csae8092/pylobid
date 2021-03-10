"""WTForms GND validator module."""
from typing import Union
import wtforms
from pylobid import pylobid

GNDWTFormsFields = Union[
    wtforms.fields.StringField,
    wtforms.fields.URLField
]


class GNDValidator:
    """Base class for GND validators.

    :param: Message to display if validation fails.
    :raises: ValidationError is the GND type does not match the set entity type.
    """

    def __init__(self, entity_flag: str = None, message: str = None) -> None:
        """Class constructor.

        :param: entity_type: The entity type to check for.
        :param message: Message to display if validation fails.
        """
        self.entity_flag = entity_flag
        self.message = message

    def __call__(self, form: wtforms.form.Form, field: GNDWTFormsFields) -> None:
        """Class call method.

        :param form: A WTForms Form instance.
        :param field: A WTForm Form Field instance.
        :raises: ValidationError is the GND type does not match the set entity type.
        """
        try:
            gnd_entity = pylobid.PyLobidClient(field.data).factory()
        except pylobid.GNDIdError as error:
            raise wtforms.validators.ValidationError(f'{field.data} is not a valid GND Id/URL') \
                from error
        except pylobid.GNDNotFoundError as error:
            raise wtforms.validators.ValidationError(error) from error
        if not gnd_entity.ent_type:
            raise wtforms.validators.ValidationError(f'Unknown GND type for {gnd_entity.gnd_url}')
        if self.entity_flag is not None and not getattr(gnd_entity, self.entity_flag, False):
            self.message = f'Entity type {gnd_entity.ent_type}'
            raise wtforms.validators.ValidationError(self.message)
