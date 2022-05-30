import os
import sys
from pathlib import Path

from tethys_apps.models import SpatialDatasetServiceSetting
from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import PersistentStoreDatabaseSetting, CustomSetting


class Wdi(TethysAppBase):
    """
    Tethys app class for Wdi.
    """

    name = 'Demanda de Agua para Irrigatción'
    index = 'wdi:home'
    icon = 'wdi/images/icon.gif'
    package = 'wdi'
    root_url = 'wdi'
    color = '#d35400'
    description = 'Calculate Water Demand for Irrigation'
    tags = '"Water Demand", "Irrigation"'
    enable_feedback = False
    feedback_emails = []

    # services
    SCHEDULER_NAME = 'remote_cluster'
    GEOSERVER_NAME = 'primary_geoserver'
    DATABASE_NAME = 'primary_db'
    FILE_DATABASE_ID_NAME = 'file_database_id'
    LINUX_CONDOR_FDB_ROOT_NAME = 'linux_condor_fdb_root'
    WINDOWS_CONDOR_FDB_ROOT_NAME = 'windows_condor_fdb_root'
    FILE_DATABASE_ROOT = os.path.join(os.path.dirname(__file__), 'workspaces', 'app_workspace', 'file_databases')

    def custom_settings(self):
        """
        Example custom_settings method.
        """
        custom_settings = (
            CustomSetting(
                name=self.FILE_DATABASE_ID_NAME,
                type=CustomSetting.TYPE_STRING,
                description='File Database ID',
                required=True
            ),
            CustomSetting(
                name=self.LINUX_CONDOR_FDB_ROOT_NAME,
                type=CustomSetting.TYPE_STRING,
                description='The File Database root directory for the Linux condor worker.',
                required=False
            ),
            CustomSetting(
                name='cesium_api_token',
                type=CustomSetting.TYPE_STRING,
                description='Cesium API Token',
                required=True
            ),
        )
        return custom_settings

    def persistent_store_settings(self):
        """
        Define persistent store settings.
        """
        ps_settings = (
            PersistentStoreDatabaseSetting(
                name='primary_db',
                description='Primary database for WDI.',
                initializer='wdi.models.init_primary_db',
                required=True,
                spatial=True,
            ),
        )

        return ps_settings

    def spatial_dataset_service_settings(self):
        """
        Define spatial dataset services settings.
        """
        sds_settings = (
            SpatialDatasetServiceSetting(
                name=self.GEOSERVER_NAME,
                description='GeoServer used to host spatial visualizations for the app.',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=True
            ),
        )
        return sds_settings

    def url_maps(self):
        """
        Add controllers
        """
        from tethysext.atcore.urls import app_users, spatial_reference, resource_workflows, resources
        from tethysapp.wdi.services.spatial_managers.wdi import WdiSpatialManager
        from tethysapp.wdi.models.resources.irrigation_zone_resource import WdiIrrigationZoneResource
        from tethysapp.wdi.models.resources.dataset_resource import WdiDatasetResource
        from tethysapp.wdi.models.resources.model_resource import WdiModelResource
        from tethysapp.wdi.models.app_users import WdiOrganization
        from tethysapp.wdi.models.wdi_workflows import WDI_WORKFLOWS

        from tethysapp.wdi.controllers.irrigation_zones import ModifyIrrigationZone, ManageIrrigationZones, \
            IrrigationZoneDetails
        from tethysapp.wdi.controllers.map_view.wdi_model_map_view import WdiModelMapView
        from tethysapp.wdi.controllers.datasets import ManageWdiDatasetResources, ModifyWdiDatasetResource, \
            WdiDatasetResourceDetails
        from tethysapp.wdi.controllers.models import ManageWdiModelResources, WdiModelResourceDetails,\
            ModifyWdiModelResource
        from tethysapp.wdi.controllers.workflows.wdi_workflow_view import WdiWorkflowRouter
        from tethysapp.wdi.services.map_manager import WdiMapManager

        UrlMap = url_map_maker(self.root_url)

        url_maps = []

        app_users_urls = app_users.urls(
            url_map_maker=UrlMap,
            app=self,
            persistent_store_name='primary_db',
            base_template='wdi/base.html',
            custom_models=(
                WdiIrrigationZoneResource,
                WdiOrganization,
            ),
            custom_controllers=(
                ManageIrrigationZones,
                ModifyIrrigationZone,
            )
        )
        url_maps.extend(app_users_urls)

        dataset_resources_urls = resources.urls(
            url_map_maker=UrlMap,
            app=self,
            persistent_store_name='primary_db',
            base_template='wdi/base.html',
            custom_models=(
                WdiDatasetResource,
            ),
            custom_controllers=(
                ManageWdiDatasetResources,
                ModifyWdiDatasetResource,
            )
        )
        url_maps.extend(dataset_resources_urls)

        model_resources_urls = resources.urls(
            url_map_maker=UrlMap,
            app=self,
            persistent_store_name='primary_db',
            base_template='wdi/base.html',
            custom_models=(
                WdiModelResource,
            ),
            custom_controllers=(
                ManageWdiModelResources,
                ModifyWdiModelResource,
            )
        )
        url_maps.extend(model_resources_urls)

        spatial_reference_urls = spatial_reference.urls(
            url_map_maker=UrlMap,
            app=self,
            persistent_store_name='primary_db'
        )
        url_maps.extend(spatial_reference_urls)

        url_maps.extend((
            UrlMap(
                name='irrigation_zone_details_tab',
                url='wdi/irrigation-zones/{resource_id}/details/{tab_slug}',
                controller=IrrigationZoneDetails.as_controller(
                    _app=self,
                    _persistent_store_name='primary_db',
                    _Organization=WdiOrganization,
                    _Resource=WdiIrrigationZoneResource
                ),
                regex=['[0-9A-Za-z-_.]+', '[0-9A-Za-z-_.{}]+']
            ),
        ))

        url_maps.extend((
            UrlMap(
                name='dataset_details_tab',
                url='wdi/datasets/{resource_id}/details/{tab_slug}',
                controller=WdiDatasetResourceDetails.as_controller(
                    _app=self,
                    _persistent_store_name='primary_db',
                    _Organization=WdiOrganization,
                    _Resource=WdiDatasetResource
                ),
                regex=['[0-9A-Za-z-_.]+', '[0-9A-Za-z-_.{}]+']
            ),
        ))

        url_maps.extend((
            UrlMap(
                name='model_details_tab',
                url='wdi/models/{resource_id}/details/{tab_slug}',
                controller=WdiModelResourceDetails.as_controller(
                    _app=self,
                    _persistent_store_name='primary_db',
                    _Organization=WdiOrganization,
                    _Resource=WdiModelResource,
                ),
                regex=['[0-9A-Za-z-_.]+', '[0-9A-Za-z-_.{}]+']
            ),
        ))

        url_maps.extend(resource_workflows.urls(
            url_map_maker=UrlMap,
            app=self,
            persistent_store_name='primary_db',
            workflow_pairs=[(workflow, WdiWorkflowRouter) for _, workflow in WDI_WORKFLOWS.items()],
            custom_models=(
                WdiIrrigationZoneResource,
                WdiOrganization
            ),
        ))

        url_maps.extend((
            UrlMap(
                name='home',
                url='',
                controller=WdiModelMapView.as_controller(
                    _app=self,
                    _persistent_store_name=self.DATABASE_NAME,
                    geoserver_name=self.GEOSERVER_NAME,
                    _Organization=WdiOrganization,
                    _Resource=WdiIrrigationZoneResource,
                    _SpatialManager=WdiSpatialManager,
                    _MapManager=WdiMapManager,
                ),
                regex=['[0-9A-Za-z-_.', '[0-9A-Za-z-_.{}]+']
            ),
        ))

        return url_maps

    def permissions(self):
        from tethysext.atcore.services.app_users.permissions_manager import AppPermissionsManager
        from tethysext.atcore.permissions.app_users import PermissionsGenerator

        # Generate permissions for App Users
        pm = AppPermissionsManager(self.namespace)
        pg = PermissionsGenerator(pm)
        permissions = pg.generate()

        return permissions

    @classmethod
    def get_job_executable_dir(cls):
        """
        Return:
             str: the path to the directory containing the job executables.
        """
        return str(Path(sys.modules['tethysapp'].wdi.__file__).parent / 'job_scripts')

    @classmethod
    def get_file_database_root(cls, relative_to='app'):
        """
        Resolve the FileDatabaseRoot relative to system given. The file database root location will vary depending on
         which system you are accessing it from.

        Args:
            relative_to (str): One of 'app', 'condor-linux', or 'condor-windows'.

        Returns:
            str: the path to the directory containing file databases.
        """  # noqa: E501
        if relative_to == 'app':
            return cls.FILE_DATABASE_ROOT

        if relative_to == 'condor-linux':
            # If the setting isn't defined, return the FDB root located in app_workspaces
            linux_fdb_root = cls.get_custom_setting(cls.LINUX_CONDOR_FDB_ROOT_NAME)
            return linux_fdb_root if linux_fdb_root else cls.FILE_DATABASE_ROOT

        elif relative_to == 'condor-windows':
            return cls.get_custom_setting(cls.WINDOWS_CONDOR_FDB_ROOT_NAME)

        return None
