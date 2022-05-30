"""
********************************************************************************
* Name: licenses.py
* Author: msouffront
* Created On: Nov 8, 2019
* Copyright: (c) Aquaveo 2019
********************************************************************************
"""
from tethysext.atcore.services.app_users.licenses import Licenses

__all__ = ['WdiLicenses']


class WdiLicenses(Licenses):
    """
    Customized license sevice for Wdi.
    """
    def list(self):
        """
        Get a list of all licenses.
        Returns:
            tuple: All available licenses.
        """
        all_licenses = (
            self.STANDARD,
            self.CONSULTANT
        )
        return all_licenses

    def must_have_consultant(self, license):
        """
        License based test to determine if an organization must be assigned a consultant.
        Args:
            license: valid license.

        Returns:
            bool: True if organization with this license must be assigned a constultant, else False
        """
        if not self.is_valid(license):
            raise ValueError('Invalid license given: {}.'.format(license))

        if license == self.STANDARD:
            return True
        elif license == self.CONSULTANT:
            return False
