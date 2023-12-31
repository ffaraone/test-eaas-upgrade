# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, CloudBlue
# All rights reserved.
#
from connect.eaas.core.decorators import event, schedulable, variables
from connect.eaas.core.extension import Extension
from connect.eaas.core.responses import (
    BackgroundResponse,
    InteractiveResponse,
    ScheduledExecutionResponse,
)

import random
import string


@variables(
    [
        {
            'name': 'ASSET_REQUEST_APPROVE_TEMPLATE_ID',
            'initial_value': '<change_with_purchase_request_approve_template_id>'
        },
        {
            'name': 'ASSET_REQUEST_CHANGE_TEMPLATE_ID',
            'initial_value': '<change_with_change_request_approve_template_id>'
        },
        {
            'name': 'TIER_REQUEST_APPROVE_TEMPLATE_ID',
            'initial_value': '<change_with_tier_request_approve_template_id>'
        },
    ],
)
class E2EExtension(Extension):

    def approve_asset_request(self, request, template_id):
        self.logger.info(f'request_id={request["id"]} - template_id={template_id}')
        self.logger.info(f'request_id={request["id"]} - template_id={template_id}')
        self.client.requests[request['id']]('approve').post(
            {
                'template_id': template_id,
            }
        )
        self.logger.info(f"Approved request {request['id']}")

    def approve_tier_request(self, request, template_id):
        self.logger.info(f'request_id={request["id"]} - template_id={template_id}')
        self.client.ns('tier').config_requests[request['id']]('approve').post(
            {
                'template': {
                    'id': template_id
                }
            }
        )
        self.logger.info(f"Approved request {request['id']}")

    @event(
        'asset_purchase_request_processing',
        statuses=[
            'pending', 'approved', 'failed', 'inquiring',
            'scheduled', 'revoking', 'revoked',
        ],
    )
    def process_asset_purchase_request(self, request):
        self.logger.info(
            f"Received event for subscription request {request['id']} in status {request['status']}"
        )
        if request['status'] == 'pending':
            param_a = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
            param_b = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
            self.client.requests[request['id']].update(
                {
                    "asset": {
                        "params": [
                            {
                                "id": "param_a",
                                "value": param_a
                            },
                            {
                                "id": "param_b",
                                "value": param_b
                            }

                        ]
                    }
                }
            )
            self.logger.info("Updating fulfillment parameters as follows:"
                             f"param_a to {param_a} and param_b to {param_b}")
            template_id = self.config['ASSET_REQUEST_APPROVE_TEMPLATE_ID']
            self.approve_asset_request(request, template_id)

        return BackgroundResponse.done()

    @event(
        'asset_change_request_processing',
        statuses=[
            'pending', 'approved', 'failed', 'inquiring',
            'scheduled', 'revoking', 'revoked',
        ],
    )
    def process_asset_change_request(self, request):
        self.logger.info(
            f"Received event for subscription request {request['id']}, type {request['type']} "
            f"in status {request['status']}"
        )

        if request['status'] == 'pending':
            template_id = self.config['ASSET_REQUEST_CHANGE_TEMPLATE_ID']
            self.approve_asset_request(request, template_id)
        return BackgroundResponse.done()

    @event(
        'asset_suspend_request_processing',
        statuses=[
            'pending', 'approved', 'failed',
            'scheduled', 'revoking', 'revoked',
        ],
    )
    def process_asset_suspend_request(self, request):
        self.logger.info(
            f"Received event for subscription request {request['id']}, type {request['type']} "
            f"in status {request['status']}"
        )
        if request['status'] == 'pending':
            template_id = self.config['ASSET_REQUEST_APPROVE_TEMPLATE_ID']
            self.approve_asset_request(request, template_id)
        return BackgroundResponse.done()

    @event(
        'asset_resume_request_processing',
        statuses=[
            'pending', 'approved', 'failed',
            'scheduled', 'revoking', 'revoked',
        ],
    )
    def process_asset_resume_request(self, request):
        self.logger.info(
            f"Received event for subscription request {request['id']}, type {request['type']} "
            f"in status {request['status']}"
        )
        if request['status'] == 'pending':
            template_id = self.config['ASSET_REQUEST_APPROVE_TEMPLATE_ID']
            self.approve_asset_request(request, template_id)
        return BackgroundResponse.done()

    @event(
        'asset_resume_cancel_processing',
        statuses=[
            'pending', 'approved', 'failed',
            'scheduled', 'revoking', 'revoked',
        ],
    )
    def process_asset_cancel_request(self, request):
        self.logger.info(
            f"Received event for subscription request {request['id']}, type {request['type']} "
            f"in status {request['status']}"
        )
        if request['status'] == 'pending':
            template_id = self.config['ASSET_REQUEST_APPROVE_TEMPLATE_ID']
            self.approve_asset_request(request, template_id)
        return BackgroundResponse.done()

    @event(
        'asset_adjustment_request_processing',
        statuses=[
            'pending', 'approved', 'failed', 'inquiring',
            'scheduled', 'revoking', 'revoked',
        ],
    )
    def process_asset_adjustment_request(self, request):
        self.logger.info(
            f"Received event for subscription request {request['id']}, type {request['type']} "
            f"in status {request['status']}"
        )
        if request['status'] == 'pending':
            template_id = self.config['ASSET_REQUEST_APPROVE_TEMPLATE_ID']
            self.approve_asset_request(request, template_id)
        return BackgroundResponse.done()

    @event('tier_config_setup_request_validation', statuses=['draft'])
    def validate_tier_config_setup_request(self, request):
        self.logger.info(f"TCR Validation with id {request['id']}")
        return InteractiveResponse.done(body=request)

    @event('tier_config_change_request_validation', statuses=['draft'])
    def validate_tier_config_change_request(self, request):
        self.logger.info(f"TCR Validation with id {request['id']}")
        return InteractiveResponse.done(body=request)

    @event('asset_purchase_request_validation', statuses=['draft'])
    def validate_asset_purchase_request(self, request):
        self.logger.info(f"Asset Validation with id {request['id']}")
        return InteractiveResponse.done(body=request)

    @event('asset_change_request_validation', statuses=['draft'])
    def validate_asset_change_request(self, request):
        self.logger.info(f"asset Validation with id {request['id']}")
        return InteractiveResponse.done(body=request)

    @event('product_action_execution')
    def execute_product_action(self, request):
        self.logger.info(f'Product action: {request}')
        return InteractiveResponse.done(
            http_status=302,
            headers={'Location': 'https://google.com'},
        )

    @event('product_custom_event_processing')
    def process_product_custom_event(self, request):
        self.logger.info(f'Custom event: {request}')
        sample_return_body = {
            "response": "OK"
        }
        return InteractiveResponse.done(body=sample_return_body)

    @event(
        'tier_config_setup_request_processing',
        statuses=['pending', 'approved', 'failed', 'inquiring'],
    )
    def process_tier_config_setup_request(self, request):
        self.logger.info(
            f"Received event for TCR request {request['id']}, type {request['type']} "
            f"in status {request['status']}",
        )
        if request['status'] == 'pending':
            reseller_fulfillment = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
            self.client.ns('tier').config_requests[request['id']].update(
                {
                    "params": [
                        {
                            "id": "reseller_fulfillment",
                            "value": reseller_fulfillment
                        }
                    ]
                }
            )
            template_id = self.config['TIER_REQUEST_APPROVE_TEMPLATE_ID']
            self.approve_tier_request(request, template_id)

        return BackgroundResponse.done()

    @event(
        'tier_config_change_request_processing',
        statuses=['pending', 'approved', 'failed', 'inquiring'],
    )
    def process_tier_config_change_request(self, request):
        self.logger.info(
            f"Received event for TCR request {request['id']}, type {request['type']} "
            f"in status {request['status']}",
        )
        if request['status'] == 'pending':
            template_id = self.config['TIER_REQUEST_APPROVE_TEMPLATE_ID']
            self.approve_tier_request(request, template_id)
        return BackgroundResponse.done()

    @event(
        'tier_config_adjustment_request_processing',
        statuses=['pending', 'approved', 'failed', 'inquiring'],
    )
    def process_tier_config_adjustment_request(self, request):
        self.logger.info(
            f"Received event for TCR request {request['id']}, type {request['type']} "
            f"in status {request['status']}",
        )
        if request['status'] == 'pending':
            template_id = self.config['TIER_REQUEST_APPROVE_TEMPLATE_ID']
            self.approve_tier_request(request, template_id)
        return BackgroundResponse.done()

    @schedulable(
        'Schedulable method mock',
        'It can be used to test DevOps scheduler.',
    )
    def execute_scheduled_processing(self, schedule):
        self.logger.info(
            f"Scheduled execution started: {schedule}",
        )
        return ScheduledExecutionResponse.done()

    @event(
        'tier_account_update_request_processing',
        statuses=['pending', 'accepted', 'ignored'],
    )
    def process_tier_account_update_request(self, request):  # pragma: no cover
        self.logger.info(
            f"Received event for tier account request  {request['id']}, type {request['type']} "
            f"in status {request['status']}",
        )
        return BackgroundResponse.done()

    @event(
        'usage_file_request_processing',
        statuses=[
            'draft', 'uploading', 'uploaded', 'invalid', 
            'processing', 'processed', 'ready', 'rejected', 
            'pending', 'accepted', 'closed',
        ],
    )  
    def process_usage_file(self, request):  # pragma: no cover
        self.logger.info(
            f"Received event for usage file  {request['id']} "
            f"in status {request['status']}",
        )
        return BackgroundResponse.done()

    @event(
        'part_usage_file_request_processing',
        statuses=['draft', 'ready', 'closed', 'failed'],
    )
    def process_usage_chunk_file(self, request):  # pragma: no cover
        self.logger.info(
            f"Received event for usage chunks file  {request['id']} "
            f"in status {request['status']}",
        )
        return BackgroundResponse.done()
