"""
********************************************************************************
* Name: organization.py
* Author: msouffront
* Created On: Nov 8, 2019
* Copyright: (c) Aquaveo 2019
********************************************************************************
"""
from tethysapp.wdi.services.licenses import WdiLicenses
from tethysext.atcore.models.app_users import Organization

__all__ = ['WdiOrganization']


class WdiOrganization(Organization):
    """
    Customized Organization model for WDI.
    """
    TYPE = 'wdi-organization'
    LICENSES = WdiLicenses()

    # Polymorphism
    __mapper_args__ = {
        'polymorphic_identity': TYPE,
    }
