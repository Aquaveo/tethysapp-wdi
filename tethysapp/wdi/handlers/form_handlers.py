from tethys_sdk.base import with_request
from tethys_apps.utilities import get_active_app
import panel as pn
from tethysext.atcore.models.app_users import ResourceWorkflowStep


@with_request
def form_handler(document):
    app = get_active_app(document.request, get_class=True)
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()

    current_step_id = document.request.url_route['kwargs']['step_id']
    current_step = session.query(ResourceWorkflowStep).get(current_step_id)
    import pdb; pdb.set_trace()
    param_class = current_step.options['param_class']
    panel = pn.Row(param_class.param, param_class.view)

    panel.server_doc(document)
