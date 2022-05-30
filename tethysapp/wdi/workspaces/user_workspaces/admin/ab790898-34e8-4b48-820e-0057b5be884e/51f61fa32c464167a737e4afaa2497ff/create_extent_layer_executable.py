#!/opt/tethys-python
import sys
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tethys_dataset_services.engines.geoserver_engine import GeoServerSpatialDatasetEngine
from tethysext.atcore.models.app_users import SpatialResource
# DO NOT REMOVE THIS LINE - EACH MODEL CLASS NEEDS TO BE IMPORTED SO SQLALCHEMY CAN FIND IT
from tethysapp.wdi.models.resources import WdiIrrigationZoneResource, WdiDatasetResource, WdiModelResource  # noqa:F401
# DO NOT REMOVE THIS LINE - EACH MODEL CLASS NEEDS TO BE IMPORTED SO SQLALCHEMY CAN FIND IT


def run(datastore_name, resource_id, resource_db_url, geoserver_endpoint, geoserver_username, geoserver_password,
        spatial_manager, status_key='create_extent_layer'):
    """
    Condor executable that creates extent layer for SpatialResources.

    Args:
        datastore_name(str): name of the already linked data store from which the layer will be created. This is usually the app database, for example: 'app_primary_db'.
        resource_id(str): ID of the Resource associated with the dataset.
        resource_db_url(str): SQLAlchemy url to the Resource database (e.g.: postgresql://postgres:pass@localhost:5432/db).
        geoserver_endpoint(str): Url to the GeoServer public endpoint (e.g.: http://localhost:8181/geoserver/rest/).
        geoserver_username(str): Administrator username for given GeoServer.
        geoserver_password(str): Administrator password for given GeoServer.
        spatial_manager(str): Dot-path to ResourceSpatialManager class for the Resource (e.g.: 'my.own.SpatialManager').
        status_key(str): Name of status key to use for status updates on the Resource.
    """  # noqa: E501
    resource = None
    resource_db_session = None

    try:
        make_session = sessionmaker()

        gs_engine = GeoServerSpatialDatasetEngine(
            endpoint=geoserver_endpoint,
            username=geoserver_username,
            password=geoserver_password
        )

        resource_db_engine = create_engine(resource_db_url)
        resource_db_session = make_session(bind=resource_db_engine)
        resource = resource_db_session.query(SpatialResource).get(resource_id)

        # Get spatial manager
        module_path, class_name = spatial_manager.rsplit('.', 1)
        SpatialManager = getattr(__import__(module_path, fromlist=[class_name]), class_name)
        spatial_manager = SpatialManager(gs_engine)
        spatial_manager.create_extent_layer(datastore_name=datastore_name, resource_id=resource_id)

        resource_db_session.refresh(resource)
        resource.set_status(status_key, SpatialResource.STATUS_SUCCESS)
        resource_db_session.commit()
        sys.stdout.write(f'\nSuccessfully created extent layer for resource ID: {resource_id}\n')

    except Exception as e:
        if resource:
            resource_db_session.refresh(resource)
            resource.set_status(status_key, SpatialResource.STATUS_ERROR)
            resource_db_session.commit()

        traceback.print_exc(file=sys.stderr)
        sys.stderr.write(type(e).__name__)
        sys.stderr.write(repr(e))
        raise e

    finally:
        resource_db_session and resource_db_session.close()


if __name__ == "__main__":
    args = sys.argv
    args.pop(0)
    run(*args)
