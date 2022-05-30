"""
********************************************************************************
* Name: flood simulation_workflow
* Author: glarsen, mlebaron
* Created On: October 17, 2019
* Copyright: (c) Aquaveo 2019
********************************************************************************
"""
import param
import os
import panel as pn

from tethysext.atcore.models.app_users import ResourceWorkflow
from tethysext.atcore.models.resource_workflow_steps import FormInputRWS, SpatialInputRWS, SpatialCondorJobRWS,\
    ResultsResourceWorkflowStep
from tethysext.atcore.models.resource_workflow_results import SpatialWorkflowResult, DatasetWorkflowResult, \
    PlotWorkflowResult, ReportWorkflowResult

from tethysapp.wdi.models.resources.irrigation_zone_resource import WdiIrrigationZoneResource


class SelectCropWatModelParam(param.Parameterized):
    DEFAULT_SETTINGS_ZONES = {
        'Santiago': {
            'Arroz Area': 114044, 'Arroz Percent First Cycle': 20, 'Arroz Percent Second Cycle': 30,
            'Arroz Percent Third Cycle': 20, 'Arroz Percent Fourth Cycle': 30, 'Arroz Efficiency': 0.2,
            'Habichuela Area': 154059, 'Habichuela Percent First Cycle': 40,
            'Habichuela Percent Second Cycle': 60, 'Habichuela Efficiency': 0.2,
            'Maiz Area': 49299, 'Maiz Percent First Cycle': 20, 'Maiz Percent Second Cycle': 30,
            'Maiz Percent Third Cycle': 20, 'Maiz Percent Fourth Cycle': 30, 'Maiz Efficiency': 0.2,
            'Sorgo Area': 320, 'Sorgo Percent First Cycle': 20, 'Sorgo Percent Second Cycle': 30,
            'Sorgo Percent Third Cycle': 20, 'Sorgo Percent Fourth Cycle': 30, 'Sorgo Efficiency': 0.2,
            'Guandul Area': 18721, 'Guandul Percent First Cycle': 40, 'Guandul Percent Second Cycle': 60,
            'Guandul Efficiency': 0.2,
            'Mani Area': 1565, 'Mani Percent First Cycle': 20, 'Mani Percent Second Cycle': 30,
            'Mani Percent Third Cycle': 20, 'Mani Percent Fourth Cycle': 30, 'Mani Efficiency': 0.2,
            'Platano Area': 583, 'Platano Percent': 100, 'Platano Efficiency': 0.2,
            'Guineo Area': 274, 'Guineo Percent': 100, 'Guineo Efficiency': 0.2,
            'Cana de Azucar Area': 30, 'Cana de Azucar Percent': 100, 'Cana de Azucar Efficiency': 0.2,
            'Cana Negra Area': 120, 'Cana Negra Percent': 100, 'Cana Negra Efficiency': 0.2,
            'Yuca Area': 4578, 'Yuca Percent First Cycle': 40, 'Yuca Percent Second Cycle': 60, 'Yuca Efficiency': 0.2,
            'Batata Area': 11052, 'Batata Percent First Cycle': 20, 'Batata Percent Second Cycle': 30,
            'Batata Percent Third Cycle': 20, 'Batata Percent Fourth Cycle': 30, 'Batata Efficiency': 0.2,
            'Tomate Area': 36, 'Tomate Percent First Cycle': 40, 'Tomate Percent Second Cycle': 60,
            'Tomate Efficiency': 0.2,
            'Cebolla Area': 13360, 'Cebolla Percent First Cycle': 40, 'Cebolla Percent Second Cycle': 60,
            'Cebolla Efficiency': 0.2,
            'Ajies Area': 1257, 'Ajies Percent First Cycle': 40, 'Ajies Percent Second Cycle': 60,
            'Ajies Efficiency': 0.2,
            'Zanahoria Area': 81, 'Zanahoria Percent First Cycle': 40, 'Zanahoria Percent Second Cycle': 60,
            'Zanahoria Efficiency': 0.2,
            'Berenjena Area': 972, 'Berenjena Percent First Cycle': 40, 'Berenjena Percent Second Cycle': 60,
            'Berenjena Efficiency': 0.2,
            'Remolacha Area': 42, 'Remolacha Percent First Cycle': 50, 'Remolacha Percent Second Cycle': 50,
            'Remolacha Efficiency': 0.2,
            'Pepino Area': 125, 'Pepino Percent First Cycle': 40, 'Pepino Percent Second Cycle': 60,
            'Pepino Efficiency': 0.2,
            'Auyama Area': 1240, 'Auyama Percent First Cycle': 20, 'Auyama Percent Second Cycle': 30,
            'Auyama Percent Third Cycle': 20, 'Auyama Percent Fourth Cycle': 30, 'Auyama Efficiency': 0.2,
            'Repollo Area': 47, 'Repollo Percent First Cycle': 40, 'Repollo Percent Second Cycle': 60,
            'Repollo Efficiency': 0.2,
            'Cilantro Area': 820,  'Cilantro Percent First Cycle': 40, 'Cilantro Percent Second Cycle': 60,
            'Cilantro Efficiency': 0.2,
            'Otras Hortalizas Area': 2400, 'Otras Hortalizas Percent First Cycle': 30,
            'Otras Hortalizas Percent Second Cycle': 30, 'Otras Hortalizas Percent Third Cycle': 40, 
            'Otras Hortalizas Efficiency': 0.2,
            'Tabaco Area': 110, 'Tabaco Percent First Cycle': 40, 'Tabaco Percent Second Cycle': 60,
            'Tabaco Efficiency': 0.2,
            'Lechosa Area': 1412, 'Lechosa Percent First Cycle': 40, 'Lechosa Percent Second Cycle': 60,
            'Lechosa Efficiency': 0.2,
            'Melon Area': 140, 'Melon Percent First Cycle': 30, 'Melon Percent Second Cycle': 40,
            'Melon Percent Third Cycle': 30, 'Melon Efficiency': 0.2,
            'Mango Area': 2425, 'Mango Percent': 100, 'Mango Efficiency': 0.2,
            'Pasto Natural Area': 13658, 'Pasto Natural Percent': 100, 'Pasto Natural Efficiency': 0.2,
        },
        'Mao': {
            'Arroz Area': 114044, 'Arroz Percent First Cycle': 20, 'Arroz Percent Second Cycle': 30,
            'Arroz Percent Third Cycle': 20, 'Arroz Percent Fourth Cycle': 30, 'Arroz Efficiency': 0.2,
            'Habichuela Area': 154059, 'Habichuela Percent First Cycle': 40,
            'Habichuela Percent Second Cycle': 60, 'Habichuela Efficiency': 0.2,
            'Maiz Area': 49299, 'Maiz Percent First Cycle': 20, 'Maiz Percent Second Cycle': 30,
            'Maiz Percent Third Cycle': 20, 'Maiz Percent Fourth Cycle': 30, 'Maiz Efficiency': 0.2,
            'Sorgo Area': 320, 'Sorgo Percent First Cycle': 20, 'Sorgo Percent Second Cycle': 30,
            'Sorgo Percent Third Cycle': 20, 'Sorgo Percent Fourth Cycle': 30, 'Sorgo Efficiency': 0.2,
            'Guandul Area': 18721, 'Guandul Percent First Cycle': 40, 'Guandul Percent Second Cycle': 60,
            'Guandul Efficiency': 0.2, 'Guandul Efficiency': 0.2,
            'Mani Area': 1565, 'Mani Percent First Cycle': 20, 'Mani Percent Second Cycle': 30,
            'Mani Percent Third Cycle': 20, 'Mani Percent Fourth Cycle': 30, 'Mani Efficiency': 0.2,
            'Platano Area': 583, 'Platano Percent': 100, 'Platano Efficiency': 0.2,
            'Guineo Area': 274, 'Guineo Percent': 100, 'Guineo Efficiency': 0.2,
            'Cana de Azucar Area': 30, 'Cana de Azucar Percent': 100, 'Cana de Azucar Efficiency': 0.2,
            'Cana Negra Area': 120, 'Cana Negra Percent': 100, 'Cana Negra Efficiency': 0.2,
            'Yuca Area': 4578, 'Yuca Percent First Cycle': 40, 'Yuca Percent Second Cycle': 60, 'Yuca Efficiency': 0.2,
            'Batata Area': 11052, 'Batata Percent First Cycle': 20, 'Batata Percent Second Cycle': 30,
            'Batata Percent Third Cycle': 20, 'Batata Percent Fourth Cycle': 30, 'Batata Efficiency': 0.2,
            'Tomate Area': 36, 'Tomate Percent First Cycle': 40, 'Tomate Percent Second Cycle': 60,
            'Tomate Efficiency': 0.2,
            'Cebolla Area': 13360, 'Cebolla Percent First Cycle': 40, 'Cebolla Percent Second Cycle': 60,
            'Cebolla Efficiency': 0.2,
            'Ajies Area': 1257, 'Ajies Percent First Cycle': 40, 'Ajies Percent Second Cycle': 60, 'Ajies Efficiency': 0.2,
            'Zanahoria Area': 81, 'Zanahoria Percent First Cycle': 40, 'Zanahoria Percent Second Cycle': 60,
            'Zanahoria Efficiency': 0.2,
            'Berenjena Area': 972, 'Berenjena Percent First Cycle': 40, 'Berenjena Percent Second Cycle': 60,
            'Berenjena Efficiency': 0.2,
            'Remolacha Area': 42, 'Remolacha Percent First Cycle': 50, 'Remolacha Percent Second Cycle': 50,
            'Remolacha Efficiency': 0.2,
            'Pepino Area': 125, 'Pepino Percent First Cycle': 40, 'Pepino Percent Second Cycle': 60, 'Pepino Efficiency': 0.2,
            'Auyama Area': 1240, 'Auyama Percent First Cycle': 20, 'Auyama Percent Second Cycle': 30,
            'Auyama Percent Third Cycle': 20, 'Auyama Percent Fourth Cycle': 30, 'Auyama Efficiency': 0.2,
            'Repollo Area': 47, 'Repollo Percent First Cycle': 40, 'Repollo Percent Second Cycle': 60,
            'Repollo Efficiency': 0.2,
            'Cilantro Area': 820, 'Cilantro Percent First Cycle': 40, 'Cilantro Percent Second Cycle': 60,
            'Cilantro Efficiency': 0.2,
            'Otras Hortalizas Area': 2400, 'Otras Hortalizas Percent First Cycle': 30,
            'Otras Hortalizas Percent Second Cycle': 30, 'Otras Hortalizas Percent Third Cycle': 40,
            'Otras Hortalizas Efficiency': 0.2,
            'Tabaco Area': 110, 'Tabaco Percent First Cycle': 40, 'Tabaco Percent Second Cycle': 60,
            'Tabaco Efficiency': 0.2,
            'Lechosa Area': 1412, 'Lechosa Percent First Cycle': 40, 'Lechosa Percent Second Cycle': 60,
            'Lechosa Efficiency': 0.2,
            'Melon Area': 140, 'Melon Percent First Cycle': 30, 'Melon Percent Second Cycle': 40,
            'Melon Percent Third Cycle': 30, 'Melon Efficiency': 0.2,
            'Mango Area': 2425, 'Mango Percent': 100, 'Mango Efficiency': 0.2,
            'Pasto Natural Area': 13658, 'Pasto Natural Percent': 100, 'Pasto Natural Efficiency': 0.2,
        },
        'Esperanza': {
            'Arroz Area': 11222, 'Arroz Percent First Cycle': 20, 'Arroz Percent Second Cycle': 30,
            'Arroz Percent Third Cycle': 20, 'Arroz Percent Fourth Cycle': 30, 'Arroz Efficiency': 0.2,
            'Habichuela Area': 5605, 'Habichuela Percent First Cycle': 40,
            'Habichuela Percent Second Cycle': 60, 'Habichuela Efficiency': 0.2,
            'Maiz Area': 13247, 'Maiz Percent First Cycle': 20, 'Maiz Percent Second Cycle': 30,
            'Maiz Percent Third Cycle': 20, 'Maiz Percent Fourth Cycle': 30, 'Maiz Efficiency': 0.2,
            'Guandul Area': 3425, 'Guandul Percent First Cycle': 40, 'Guandul Percent Second Cycle': 60,
            'Guandul Efficiency': 0.2, 'Guandul Efficiency': 0.2,
            'Mani Area': 3253, 'Mani Percent First Cycle': 20, 'Mani Percent Second Cycle': 30,
            'Mani Percent Third Cycle': 20, 'Mani Percent Fourth Cycle': 30, 'Mani Efficiency': 0.2,
            'Platano Area': 2299, 'Platano Percent': 100, 'Platano Efficiency': 0.2,
            'Guineo Area': 119, 'Guineo Percent': 100, 'Guineo Efficiency': 0.2,
            'Cana de Azucar Area': 85, 'Cana de Azucar Percent': 100, 'Cana de Azucar Efficiency': 0.2,
            'Yuca Area': 2303, 'Yuca Percent First Cycle': 40, 'Yuca Percent Second Cycle': 60,
            'Yuca Efficiency': 0.2,
            'Batata Area': 3934, 'Batata Percent First Cycle': 20, 'Batata Percent Second Cycle': 30,
            'Batata Percent Third Cycle': 20, 'Batata Percent Fourth Cycle': 30, 'Batata Efficiency': 0.2,
            'Cebolla Area': 23, 'Cebolla Percent First Cycle': 40, 'Cebolla Percent Second Cycle': 60,
            'Cebolla Efficiency': 0.2,
            'Ajies Area': 176, 'Ajies Percent First Cycle': 40, 'Ajies Percent Second Cycle': 60,
            'Ajies Efficiency': 0.2,
            'Berenjena Area': 488, 'Berenjena Percent First Cycle': 40, 'Berenjena Percent Second Cycle': 60,
            'Berenjena Efficiency': 0.2,
            'Remolacha Area': 64, 'Remolacha Percent First Cycle': 50, 'Remolacha Percent Second Cycle': 50,
            'Remolacha Efficiency': 0.2,
            'Pepino Area': 88, 'Pepino Percent First Cycle': 40, 'Pepino Percent Second Cycle': 60,
            'Pepino Efficiency': 0.2,
            'Auyama Area': 895, 'Auyama Percent First Cycle': 20, 'Auyama Percent Second Cycle': 30,
            'Auyama Percent Third Cycle': 20, 'Auyama Percent Fourth Cycle': 30, 'Auyama Efficiency': 0.2,
            'Cilantro Area': 690, 'Cilantro Percent First Cycle': 40, 'Cilantro Percent Second Cycle': 60,
            'Cilantro Efficiency': 0.2,
            'Otras Hortalizas Area': 616, 'Otras Hortalizas Percent First Cycle': 30,
            'Otras Hortalizas Percent Second Cycle': 30, 'Otras Hortalizas Percent Third Cycle': 40,
            'Otras Hortalizas Efficiency': 0.2,
            'Tabaco Area': 226, 'Tabaco Percent First Cycle': 40, 'Tabaco Percent Second Cycle': 60,
            'Tabaco Efficiency': 0.2,
            'Lechosa Area': 30, 'Lechosa Percent First Cycle': 40, 'Lechosa Percent Second Cycle': 60,
            'Lechosa Efficiency': 0.2,
            'Pasto Natural Area': 1169, 'Pasto Natural Percent': 100, 'Pasto Natural Efficiency': 0.2,
        },
        'La_Isabela': {
            'Arroz Area': 11222, 'Arroz Percent First Cycle': 20, 'Arroz Percent Second Cycle': 30,
            'Arroz Percent Third Cycle': 20, 'Arroz Percent Fourth Cycle': 30, 'Arroz Efficiency': 0.2,
            'Habichuela Area': 5605, 'Habichuela Percent First Cycle': 40,
            'Habichuela Percent Second Cycle': 60, 'Habichuela Efficiency': 0.2,
            'Maiz Area': 13247, 'Maiz Percent First Cycle': 20, 'Maiz Percent Second Cycle': 30,
            'Maiz Percent Third Cycle': 20, 'Maiz Percent Fourth Cycle': 30, 'Maiz Efficiency': 0.2,
            'Guandul Area': 3425, 'Guandul Percent First Cycle': 40, 'Guandul Percent Second Cycle': 60,
            'Guandul Efficiency': 0.2, 'Guandul Efficiency': 0.2,
            'Mani Area': 3253, 'Mani Percent First Cycle': 20, 'Mani Percent Second Cycle': 30,
            'Mani Percent Third Cycle': 20, 'Mani Percent Fourth Cycle': 30, 'Mani Efficiency': 0.2,
            'Platano Area': 2299, 'Platano Percent': 100, 'Platano Efficiency': 0.2,
            'Guineo Area': 119, 'Guineo Percent': 100, 'Guineo Efficiency': 0.2,
            'Cana de Azucar Area': 85, 'Cana de Azucar Percent': 100, 'Cana de Azucar Efficiency': 0.2,
            'Yuca Area': 2303, 'Yuca Percent First Cycle': 40, 'Yuca Percent Second Cycle': 60, 'Yuca Efficiency': 0.2,
            'Batata Area': 3934, 'Batata Percent First Cycle': 20, 'Batata Percent Second Cycle': 30,
            'Batata Percent Third Cycle': 20, 'Batata Percent Fourth Cycle': 30, 'Batata Efficiency': 0.2,
            'Cebolla Area': 23, 'Cebolla Percent First Cycle': 40, 'Cebolla Percent Second Cycle': 60,
            'Cebolla Efficiency': 0.2,
            'Ajies Area': 176, 'Ajies Percent First Cycle': 40, 'Ajies Percent Second Cycle': 60,
            'Ajies Efficiency': 0.2,
            'Berenjena Area': 488, 'Berenjena Percent First Cycle': 40, 'Berenjena Percent Second Cycle': 60,
            'Berenjena Efficiency': 0.2,
            'Remolacha Area': 64, 'Remolacha Percent First Cycle': 50, 'Remolacha Percent Second Cycle': 50,
            'Remolacha Efficiency': 0.2,
            'Pepino Area': 88, 'Pepino Percent First Cycle': 40, 'Pepino Percent Second Cycle': 60,
            'Pepino Efficiency': 0.2,
            'Auyama Area': 895, 'Auyama Percent First Cycle': 20, 'Auyama Percent Second Cycle': 30,
            'Auyama Percent Third Cycle': 20, 'Auyama Percent Fourth Cycle': 30, 'Auyama Efficiency': 0.2,
            'Cilantro Area': 690, 'Cilantro Percent First Cycle': 40, 'Cilantro Percent Second Cycle': 60,
            'Cilantro Efficiency': 0.2,
            'Otras Hortalizas Area': 616, 'Otras Hortalizas Percent First Cycle': 30,
            'Otras Hortalizas Percent Second Cycle': 30, 'Otras Hortalizas Percent Third Cycle': 40,
            'Otras Hortalizas Efficiency': 0.2,
            'Tabaco Area': 226, 'Tabaco Percent First Cycle': 40, 'Tabaco Percent Second Cycle': 60,
            'Tabaco Efficiency': 0.2,
            'Lechosa Area': 30, 'Lechosa Percent First Cycle': 40, 'Lechosa Percent Second Cycle': 60,
            'Lechosa Efficiency': 0.2,
            'Pasto Natural Area': 1169, 'Pasto Natural Percent': 100, 'Pasto Natural Efficiency': 0.2,
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(SelectCropWatModelParam, self).__init__(*args, **kwargs)
        if 'request' in kwargs:
            self.update_param_data(**kwargs)

    select_existing_cropwat_model = param.ObjectSelector(default='default_string', precedence=1, objects=['default_string'],
                                                  label="Select Existing CropWat Model")
    
    arroz_area = param.Parameter(default=-10000, pickle_default_value=False, precedence=2, label='Arroz Area')
    arroz_percent_first_cycle = param.Parameter(default=-20, precedence=3, label='Arroz Percent First Cycle')
    arroz_percent_second_cycle = param.Parameter(default=-20, precedence=4, label='Arroz Percent Second Cycle')
    arroz_percent_third_cycle = param.Parameter(default=-20, precedence=5, label='Arroz Percent Third Cycle')
    arroz_percent_fourth_cycle = param.Parameter(default=-20, precedence=6, label='Arroz Percent Fourth Cycle')
    arroz_efficiency = param.Parameter(default=-0.2, precedence=7, label='Arroz Efficiency')

    habichuela_area = param.Parameter(default=-10000, precedence=8, label='Habichuela Area')
    habichuela_percent_first_cycle = param.Parameter(default=-20, precedence=9, label='Habichuela Percent First Cycle')
    habichuela_percent_second_cycle = param.Parameter(default=-20, precedence=10,
                                                      label='Habichuela Percent Second Cycle')
    habichuela_efficiency = param.Parameter(default=-0.2, precedence=11, label='Habichuela Efficiency')

    maiz_area = param.Parameter(default=-100003, precedence=-1, label='Maiz Area')
    maiz_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Maiz Percent First Cycle')
    maiz_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Maiz Percent Second Cycle')
    maiz_percent_third_cycle = param.Parameter(default=-20, precedence=-1, label='Maiz Percent Third Cycle')
    maiz_percent_fourth_cycle = param.Parameter(default=-20, precedence=-1, label='Maiz Percent Fourth Cycle')
    maiz_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Maiz Efficiency')

    sorgo_area = param.Parameter(default=-100004, precedence=-1, label='Sorgo Area')
    sorgo_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Sorgo Percent First Cycle')
    sorgo_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Sorgo Percent Second Cycle')
    sorgo_percent_third_cycle = param.Parameter(default=-20, precedence=-1, label='Sorgo Percent Third Cycle')
    sorgo_percent_fourth_cycle = param.Parameter(default=-20, precedence=-1, label='Sorgo Percent Fourth Cycle')
    sorgo_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Sorgo Efficiency')

    guandul_area = param.Parameter(default=-100000, precedence=-1, label='Guandul Area')
    guandul_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Guandul Percent First Cycle')
    guandul_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Guandul Percent Second Cycle')
    guandul_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Guandul Efficiency')

    mani_area = param.Parameter(default=-100000, precedence=-1, label='Mani Area')
    mani_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Mani Percent First Cycle')
    mani_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Mani Percent Second Cycle')
    mani_percent_third_cycle = param.Parameter(default=-20, precedence=-1, label='Mani Percent Third Cycle')
    mani_percent_fourth_cycle = param.Parameter(default=-20, precedence=-1, label='Mani Percent Fourth Cycle')
    mani_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Mani Efficiency')

    platano_area = param.Parameter(default=-100000, precedence=-1, label='Platano Area')
    platano_percent = param.Parameter(default=-100, precedence=-1, label='Platano Percent')
    platano_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Platano Efficiency')

    guineo_area = param.Parameter(default=-100000, precedence=-1, label='Guineo Area')
    guineo_percent = param.Parameter(default=-100, precedence=-1, label='Guineo Percent')
    guineo_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Guineo Efficiency')

    cana_de_azucar_area = param.Parameter(default=-100000, precedence=-1, label='Cana de Azucar Area')
    cana_de_azucar_percent = param.Parameter(default=-100, precedence=-1, label='Cana de Azucar Percent')
    cana_de_azucar_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Cana de Azucar Efficiency')

    cana_negra_area = param.Parameter(default=-100000, precedence=-1, label='Cana Negra Area')
    cana_negra_percent = param.Parameter(default=-100, precedence=-1, label='Cana Negra Percent')
    cana_negra_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Cana Negra Efficiency')
    
    yuca_area = param.Parameter(default=-100000, precedence=-1, label='Yuca Area')
    yuca_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Yuca Percent First Cycle')
    yuca_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Yuca Percent Second Cycle')
    yuca_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Yuca Efficiency')

    batata_area = param.Parameter(default=-100000, precedence=-1, label='Batata Area')
    batata_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Batata Percent First Cycle')
    batata_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Batata Percent Second Cycle')
    batata_percent_third_cycle = param.Parameter(default=-20, precedence=-1, label='Batata Percent Third Cycle')
    batata_percent_fourth_cycle = param.Parameter(default=-20, precedence=-1, label='Batata Percent Fourth Cycle')
    batata_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Batata Efficiency')

    tomate_area = param.Parameter(default=-100000, precedence=-1, label='Tomate Area')
    tomate_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Tomate Percent First Cycle')
    tomate_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Tomate Percent Second Cycle')
    tomate_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Tomate Efficiency')

    cebolla_area = param.Parameter(default=-100000, precedence=-1, label='Cebolla Area')
    cebolla_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Cebolla Percent First Cycle')
    cebolla_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Cebolla Percent Second Cycle')
    cebolla_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Cebolla Efficiency')

    ajies_area = param.Parameter(default=-100000, precedence=-1, label='Ajies Area')
    ajies_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Ajies Percent First Cycle')
    ajies_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Ajies Percent Second Cycle')
    ajies_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Ajies Efficiency')

    zanahoria_area = param.Parameter(default=-100000, precedence=-1, label='Zanahoria Area')
    zanahoria_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Zanahoria Percent First Cycle')
    zanahoria_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Zanahoria Percent Second Cycle')
    zanahoria_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Zanahoria Efficiency')

    berenjena_area = param.Parameter(default=-100000, precedence=-1, label='Berenjena Area')
    berenjena_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Berenjena Percent First Cycle')
    berenjena_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Berenjena Percent Second Cycle')
    berenjena_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Berenjena Efficiency')

    remolacha_area = param.Parameter(default=-100000, precedence=-1, label='Remolacha Area')
    remolacha_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Remolacha Percent First Cycle')
    remolacha_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Remolacha Percent Second Cycle')
    remolacha_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Remolacha Efficiency')

    pepino_area = param.Parameter(default=-100000, precedence=-1, label='Pepino Area')
    pepino_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Pepino Percent First Cycle')
    pepino_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Pepino Percent Second Cycle')
    pepino_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Pepino Efficiency')

    auyama_area = param.Parameter(default=-100000, precedence=-1, label='Auyama Area')
    auyama_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Auyama Percent First Cycle')
    auyama_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Auyama Percent Second Cycle')
    auyama_percent_third_cycle = param.Parameter(default=-20, precedence=-1, label='Auyama Percent Third Cycle')
    auyama_percent_fourth_cycle = param.Parameter(default=-20, precedence=-1, label='Auyama Percent Fourth Cycle')
    auyama_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Auyama Efficiency')

    repollo_area = param.Parameter(default=-100000, precedence=-1, label='Repollo Area')
    repollo_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Repollo Percent First Cycle')
    repollo_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Repollo Percent Second Cycle')
    repollo_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Repollo Efficiency')

    cilantro_area = param.Parameter(default=-100000, precedence=-1, label='Cilantro Area')
    cilantro_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Cilantro Percent First Cycle')
    cilantro_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Cilantro Percent Second Cycle')
    cilantro_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Cilantro Efficiency')

    otras_hortalizas_area = param.Parameter(default=-100000, precedence=-1, label='Otras Hortalizas Area')
    otras_hortalizas_percent_first_cycle = param.Parameter(default=-20, precedence=-1,
                                                           label='Otras Hortalizas Percent First Cycle')
    otras_hortalizas_percent_second_cycle = param.Parameter(default=-20, precedence=-1,
                                                            label='Otras Hortalizas Percent Second Cycle')
    otras_hortalizas_percent_third_cycle = param.Parameter(default=-20, precedence=-1,
                                                           label='Otras Hortalizas Percent Third Cycle')
    otras_hortalizas_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Otras Hortalizas Efficiency')

    tabaco_area = param.Parameter(default=-100000, precedence=-1, label='Tabaco Area')
    tabaco_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Tabaco Percent First Cycle')
    tabaco_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Tabaco Percent Second Cycle')
    tabaco_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Tabaco Efficiency')

    lechosa_area = param.Parameter(default=-100000, precedence=-1, label='Lechosa Area')
    lechosa_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Lechosa Percent First Cycle')
    lechosa_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Lechosa Percent Second Cycle')
    lechosa_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Lechosa Efficiency')

    melon_area = param.Parameter(default=-100000, precedence=-1, label='Melon Area')
    melon_percent_first_cycle = param.Parameter(default=-20, precedence=-1, label='Melon Percent First Cycle')
    melon_percent_second_cycle = param.Parameter(default=-20, precedence=-1, label='Melon Percent Second Cycle')
    melon_percent_third_cycle = param.Parameter(default=-20, precedence=-1, label='Melon Percent Third Cycle')
    melon_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Melon Efficiency')

    mango_area = param.Parameter(default=-100000, precedence=-1, label='Mango Area')
    mango_percent = param.Parameter(default=-100, precedence=-1, label='Mango Percent')
    mango_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Mango Efficiency')

    pasto_natural_area = param.Parameter(default=-100000, precedence=-1, label='Pasto Natural Area')
    pasto_natural_percent = param.Parameter(default=-100, precedence=-1, label='Pasto Natural Percent')
    pasto_natural_efficiency = param.Parameter(default=-0.2, precedence=-1, label='Pasto Natural Efficiency')

    def update_param_data(self, **kwargs):
        """
            This method will update the base_scenario and existing scenario using the existing model intersecting with
            the irrigation zone.
        """
        if kwargs:
            workflow_id = None
            if kwargs['request'].resolver_match:
                resource_id = kwargs['request'].resolver_match.kwargs['resource_id']
            else:
                resource_id = kwargs['request'].url_route['kwargs']['resource_id']
                workflow_id = kwargs['request'].url_route['kwargs']['workflow_id']
            session = kwargs['session']
            resource = session.query(WdiIrrigationZoneResource).get(resource_id)
            workflow = session.query(ResourceWorkflow).get(workflow_id)
            select_existing_cropwat_models = dict()
            model_name_duplicate_count = 0
            for model in resource.models:
                model_name = str(model.name)
                if str(model.name) in select_existing_cropwat_models.keys():
                    model_name_duplicate_count += 1
                    model_name = f'{model_name} {model_name_duplicate_count}'
                select_existing_cropwat_models[model_name] = str(model.id)

            param_update_list = ['select_existing_cropwat_model']
            for each_param in param_update_list:
                self.param[each_param].default = list(select_existing_cropwat_models.values())[0]
                self.param[each_param].names = select_existing_cropwat_models
                self.param[each_param].objects = list(select_existing_cropwat_models.values())

            zone_param_update_list = \
                ['Arroz Area', 'Arroz Percent First Cycle', 'Arroz Percent Second Cycle', 'Arroz Percent Third Cycle',
                 'Arroz Percent Fourth Cycle', 'Arroz Efficiency', 'Habichuela Area', 'Habichuela Percent First Cycle',
                 'Habichuela Percent Second Cycle', 'Habichuela Efficiency', 'Maiz Area', 'Maiz Percent First Cycle',
                 'Maiz Percent Second Cycle', 'Maiz Percent Third Cycle', 'Maiz Percent Fourth Cycle',
                 'Maiz Efficiency', 'Sorgo Area', 'Sorgo Percent First Cycle', 'Sorgo Percent Second Cycle',
                 'Sorgo Percent Third Cycle', 'Sorgo Percent Fourth Cycle', 'Sorgo Efficiency', 'Guandul Area',
                 'Guandul Percent First Cycle', 'Guandul Percent Second Cycle', 'Guandul Efficiency', 'Mani Area',
                 'Mani Percent First Cycle', 'Mani Percent Second Cycle', 'Mani Percent Third Cycle',
                 'Mani Percent Fourth Cycle', 'Mani Efficiency', 'Platano Area', 'Platano Percent',
                 'Platano Efficiency', 'Guineo Area', 'Guineo Percent', 'Guineo Efficiency', 'Cana de Azucar Area',
                 'Cana de Azucar Percent', 'Cana de Azucar Efficiency', 'Cana Negra Area', 'Cana Negra Percent',
                 'Cana Negra Efficiency', 'Yuca Area', 'Yuca Percent First Cycle', 'Yuca Percent Second Cycle',
                 'Yuca Efficiency', 'Batata Area', 'Batata Percent First Cycle', 'Batata Percent Second Cycle',
                 'Batata Percent Third Cycle', 'Batata Percent Fourth Cycle', 'Batata Efficiency', 'Tomate Area',
                 'Tomate Percent First Cycle', 'Tomate Percent Second Cycle', 'Tomate Efficiency', 'Cebolla Area',
                 'Cebolla Percent First Cycle', 'Cebolla Percent Second Cycle', 'Cebolla Efficiency', 'Ajies Area',
                 'Ajies Percent First Cycle', 'Ajies Percent Second Cycle', 'Ajies Efficiency', 'Zanahoria Area',
                 'Zanahoria Percent First Cycle', 'Zanahoria Percent Second Cycle', 'Zanahoria Efficiency',
                 'Berenjena Area', 'Berenjena Percent First Cycle', 'Berenjena Percent Second Cycle',
                 'Berenjena Efficiency', 'Remolacha Area', 'Remolacha Percent First Cycle',
                 'Remolacha Percent Second Cycle', 'Remolacha Efficiency', 'Pepino Area',
                 'Pepino Percent First Cycle', 'Pepino Percent Second Cycle', 'Pepino Efficiency', 'Auyama Area',
                 'Auyama Percent First Cycle', 'Auyama Percent Second Cycle', 'Auyama Percent Third Cycle',
                 'Auyama Percent Fourth Cycle', 'Auyama Efficiency', 'Repollo Area', 'Repollo Percent First Cycle',
                 'Repollo Percent Second Cycle', 'Repollo Efficiency', 'Cilantro Area', 'Cilantro Percent First Cycle',
                 'Cilantro Percent Second Cycle', 'Cilantro Efficiency', 'Otras Hortalizas Area',
                 'Otras Hortalizas Percent First Cycle', 'Otras Hortalizas Percent Second Cycle',
                 'Otras Hortalizas Percent Third Cycle', 'Otras Hortalizas Efficiency', 'Tabaco Area',
                 'Tabaco Percent First Cycle', 'Tabaco Percent Second Cycle', 'Tabaco Efficiency',
                 'Lechosa Area', 'Lechosa Percent First Cycle', 'Lechosa Percent Second Cycle',
                 'Lechosa Efficiency', 'Melon Area', 'Melon Percent First Cycle', 'Melon Percent Second Cycle',
                 'Melon Percent Third Cycle', 'Melon Efficiency', 'Mango Area', 'Mango Percent', 'Mango Efficiency',
                 'Pasto Natural Area', 'Pasto Natural Percent', 'Pasto Natural Efficiency']

            resource_name = resource.name
            if 'mao' in resource_name.lower():
                zone_name = 'Mao'
            elif 'santiago' in resource_name.lower():
                zone_name = 'Santiago'
            elif 'esperanza' in resource_name.lower():
                zone_name = 'Esperanza'
            elif 'isabela' in resource_name.lower():
                zone_name = 'La_Isabela'
            for each_zone_param in zone_param_update_list:
                zone_param_name = each_zone_param.replace(" ", "_").lower()
                # This is how you set default value
                if each_zone_param in self.DEFAULT_SETTINGS_ZONES[zone_name]:
                    setattr(self, zone_param_name, self.DEFAULT_SETTINGS_ZONES[zone_name][each_zone_param])
                else:
                    self.param[zone_param_name].precedence = -1


ops = SelectCropWatModelParam()
op = pn.panel(ops.param)
pn.Param(SelectCropWatModelParam, default_layout=pn.Row, width=900, show_name=False)
print(pn.panel(ops.param))
print(op)


CropWatParamView = pn.Param(
    SelectCropWatModelParam,
    parameters=['select_existing_cropwat_model', 'arroz_area', 'arroz_percent_first_cycle',
                'arroz_percent_second_cycle'],
    show_name=False,
    default_layout=pn.Row,
    width=600,
)

class PrepareCropWatWorkflow(ResourceWorkflow):
    """
    Data model for storing information about detention basin workflows.
    """
    TYPE = 'prepare_cropwat_demo'
    DISPLAY_TYPE_SINGULAR = 'Prepare Cropwat Workflow'
    DISPLAY_TYPE_PLURAL = 'Prepare Cropwat Workflow'

    __mapper_args__ = {
        'polymorphic_identity': TYPE
    }

    def get_url_name(self):
        return 'wdi:prepare_cropwat_demo_workflow'

    @classmethod
    def new(cls, app, name, resource_id, creator_id, geoserver_name, map_manager, spatial_manager, **kwargs):
        """
        Factor class method that creates a new workflow with steps
        Args:
            app:
            name:
            resource_id:
            creator_id:
            kwargs: additional arguments to use when configuring workflows.

        Returns:
            ResourceWorkflow: the new workflow.
        """
        # Create new workflow instance
        workflow = cls(name=name, resource_id=resource_id, creator_id=creator_id)

        # Set workflow attributes
        workflow.set_attribute('file_database_id', app.get_custom_setting(app.FILE_DATABASE_ID_NAME))
        workflow.set_attribute('linux_fdb_root', app.get_file_database_root(relative_to='condor-linux'))

        # Setup Create Detention Basins Step
        step1 = FormInputRWS(
            name='Update Model Input',
            order=10,
            help='Select CropWat Model and Update Model Input',
            options={
                'param_class': 'tethysapp.wdi.models.wdi_workflows.'
                               'prepare_cropwat_demo.SelectCropWatModelParam',
                'form_title': 'Update Model Input',
                'renderer': 'bokeh'
            }
        )
        workflow.steps.append(step1)

        job_executable_dir = app.get_job_executable_dir()

        run_cropwat_model = {
            'name': 'run_cropwat_model',
            'condorpy_template_name': 'vanilla_transfer_files',
            'remote_input_files': [
                os.path.join(job_executable_dir, 'workflows', 'prepare_cropwat_demo',
                             'run_cropwat_model.py'),
            ],
            'attributes': {
                'executable': 'run_cropwat_model.py',
            }
        }

        prepare_results = {
            'name': 'prepare_results',
            'condorpy_template_name': 'vanilla_transfer_files',
            'remote_input_files': [
                os.path.join(job_executable_dir, 'workflows', 'prepare_cropwat_demo',
                             'prepare_results.py'),
            ],
            'attributes': {
                'executable': 'prepare_results.py',
            },
            'parents': [run_cropwat_model['name']],
        }

        step2 = SpatialCondorJobRWS(
            name='Review CropWat Input',
            order=30,
            help='Review selected CropWat model and press the Run button to run the simulation. Press the Next button'
                 ' after execution as finished',
            options={
                'scheduler': app.SCHEDULER_NAME,
                'jobs': [run_cropwat_model, prepare_results],
                'working_message': 'Model is running.',
                'error_message': 'Job failed.',
                'pending_message': 'Run model to continue.',
                'geocode_enabled': False,
            },
            geoserver_name=geoserver_name,
            map_manager=map_manager,
            spatial_manager=spatial_manager,
        )
        workflow.steps.append(step2)

        # Verify Results
        step3 = ResultsResourceWorkflowStep(
            name='Preview Results',
            order=40,
            help='Use the tabs near the bottom on the screen to view each result',
        )
        workflow.steps.append(step3)
        step2.result = step3

        review_results_1 = DatasetWorkflowResult(
            name='CropWat Result',
            codename='cropwat_table',
            order=30,
            options={
                'no_dataset_message': 'No data to view...',
            },
        )

        review_results_2 = PlotWorkflowResult(
            name='Gross Irrigation Demand',
            codename='gross_demand',
            order=30,
            options={
                'no_dataset_message': 'No data to view...',
                'renderer': 'plotly',
                'plot_type': 'lines',
                'line_shape': 'spline',
                'axis_labels': ['Time', 'Depth (ft)'],
            },
        )

        review_results_3 = SpatialWorkflowResult(
            name='Map Demand',
            codename='map_demand',
            order=20,
            options={
                'layer_group_title': 'Map Demand',
            },
            geoserver_name=geoserver_name,
            map_manager=map_manager,
            spatial_manager=spatial_manager,
        )
        step3.results.extend([review_results_1, review_results_2, review_results_3])

        return workflow
