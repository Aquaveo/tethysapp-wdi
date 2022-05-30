from tethysext.atcore.services.resource_spatial_manager import ResourceSpatialManager

from .base import DatasetSpatialManager, IrrigationZoneSpatialManager

__all__ = ['WdiSpatialManager', 'WdiDatasetSpatialManager', 'WdiIrrigationZoneSpatialManager']


class WdiSpatialManager(ResourceSpatialManager):
    WORKSPACE = 'wdi'
    URI = 'http://app.aquaveo.com/wdi'
    DATASTORE = 'wdi_primary_db'


class WdiDatasetSpatialManager(DatasetSpatialManager, WdiSpatialManager):
    pass


class WdiIrrigationZoneSpatialManager(IrrigationZoneSpatialManager, WdiSpatialManager):
    pass
