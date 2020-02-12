# -*- coding: utf-8 -*-

import click
# OLI Box config


@click.command()
@click.option('--oli_box_id', prompt='oli box id', help='Oli box ID')
@click.option('--project_id', prompt='project id', help='Project ID')
@click.option('--device_type', prompt='device type', help='Device type')
def config_oli_box(oli_box_id, project_id, device_type):
    """
    Basic information about OLI box.
    """

    obj = {}
    obj['oli_box_id'] = oli_box_id
    obj['project_id'] = project_id
    obj['device_type'] = device_type
    return (obj)
