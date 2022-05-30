"""
* Name: irrigation_zone_details.py
* Author: msouffront, htran
* Created On: December 23, 2020
* Copyright: (c) Aquaveo 2020
********************************************************************************
"""
__all__ = ['WdiDatasetResourceDetails']

from tethysext.atcore.controllers.resources import TabbedResourceDetails
from tethysapp.wdi.controllers.datasets.tabs import DatasetSummaryTab, DatasetFilesTab


class WdiDatasetResourceDetails(TabbedResourceDetails):
    """
    Controller for Dataset details page(s).
    """
    base_template = 'wdi/base.html'
    tabs = (
        {'slug': 'summary', 'title': 'Summary', 'view': DatasetSummaryTab},
        {'slug': 'files', 'title': 'Files', 'view': DatasetFilesTab},
    )
