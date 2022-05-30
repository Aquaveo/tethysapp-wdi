"""
* Name: model_resource_details.py
* Author: msouffront, htran
* Created On: January 26, 2021
* Copyright: (c) Aquaveo 2021
********************************************************************************
"""
__all__ = ['WdiModelResourceDetails']

from tethysext.atcore.controllers.resources import TabbedResourceDetails
from tethysapp.wdi.controllers.models.tabs import ModelFilesTab, ModelSummaryTab


class WdiModelResourceDetails(TabbedResourceDetails):
    """
    Controller for Model details page(s).
    """
    base_template = 'wdi/base.html'
    tabs = (
        {'slug': 'summary', 'title': 'Summary', 'view': ModelSummaryTab},
        {'slug': 'files', 'title': 'Files', 'view': ModelFilesTab},
    )
