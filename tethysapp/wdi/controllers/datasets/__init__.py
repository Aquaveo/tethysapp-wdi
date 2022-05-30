"""
********************************************************************************
* Name: __init__.py
* Author: msouffront, htran
* Created On: Nov 23, 2020
* Copyright: (c) Aquaveo 2020
********************************************************************************
"""
from tethysapp.wdi.controllers.datasets.manage_dataset_resources import ManageWdiDatasetResources  # noqa:401
from tethysapp.wdi.controllers.datasets.modify_dataset_resources import ModifyWdiDatasetResource  # noqa:401
from tethysapp.wdi.controllers.datasets.dataset_resource_details import WdiDatasetResourceDetails  # noqa:401
from tethysapp.wdi.controllers.datasets.tabs.dataset_files_tab import DatasetFilesTab  # noqa:401
from tethysapp.wdi.controllers.datasets.tabs.dataset_summary_tab import DatasetSummaryTab  # noqa:401
