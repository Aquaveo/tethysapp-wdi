"""
********************************************************************************
* Name: irrigation_zone_workflows_tab.py
* Author: gagelarsen
* Created On: December 02, 2020
* Copyright: (c) Aquaveo 2020
********************************************************************************
"""
from tethysext.atcore.controllers.resources import ResourceWorkflowsTab
from tethysapp.wdi.models.wdi_workflows import WDI_WORKFLOWS
from tethysapp.wdi.services.spatial_managers.wdi import WdiSpatialManager

from tethysapp.wdi.services.map_manager import WdiMapManager


class IrrigationZoneWorkflowsTab(ResourceWorkflowsTab):

    @classmethod
    def get_workflow_types(cls):
        return WDI_WORKFLOWS

    def get_map_manager(self):
        return WdiMapManager

    def get_spatial_manager(self):
        return WdiSpatialManager

    def get_sds_setting_name(self):
        return self.get_app().GEOSERVER_NAME
