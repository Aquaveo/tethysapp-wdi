import logging

from django.shortcuts import reverse

from tethysext.atcore.controllers.app_users import ManageResources
from tethysext.atcore.mixins.file_collection_controller_mixin import FileCollectionsControllerMixin
from tethysapp.wdi.services.spatial_managers.wdi import WdiSpatialManager

from tethysapp.wdi.app import Wdi as app

log = logging.getLogger(f'tethys.{__name__}')


class ManageWdiDatasetResources(ManageResources, FileCollectionsControllerMixin):
    """
    Controller for manage_resources page.
    """
    base_template = 'wdi/base.html'

    def get_launch_url(self, request, resource):
        """
        Get the URL for the Resource Launch button.
        """
        return reverse('wdi:dataset_details_tab', args=[resource.id, 'summary'])

    def get_error_url(self, request, resource):
        """
        Get the URL for the Resource Launch button.
        """
        return reverse('wdi:dataset_details_tab', args=[resource.id, 'summary'])

    def perform_custom_delete_operations(self, session, request, resource):
        """
        Hook to perform custom delete operations prior to the resource being deleted.

        Args:
            session(sqlalchemy.session): open sqlalchemy session.
            request(django.Request): the DELETE request object.
            resource(Resource): the sqlalchemy Resource instance to be deleted.

        Raises:
            Exception: raise an appropriate exception if an error occurs. The message will be sent as the 'error' field of the JsonResponse.
        """  # noqa: E501
        self.delete_file_collections(
            session=session,
            resource=resource,
            log=log
        )

        # Delete extent layer
        gs_engine = app.get_spatial_dataset_service(app.GEOSERVER_NAME, as_engine=True)
        wdi_spatial_manager = WdiSpatialManager(gs_engine)
        wdi_spatial_manager.delete_extent_layer(
            datastore_name=WdiSpatialManager.DATASTORE,
            resource_id=str(resource.id),
        )
