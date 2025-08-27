import asyncio
import logging
from uuid import uuid4

import httpx

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    MessageSendParams,
    MessageSendConfiguration,
    SendMessageRequest,
    SendStreamingMessageRequest,
)

async def test_different_modes():
    """test different processing modes"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    base_url = 'http://localhost:9999'

    async with httpx.AsyncClient() as httpx_client:
        # get agent card
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
        agent_card = await resolver.get_agent_card()
        
        # create client
        client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)
        
        # test 1: simple mode
        logger.info("=" * 60)
        logger.info("test 1: simple mode")
        logger.info("=" * 60)
        
        simple_payload = {
            'message': {
                'role': 'user',
                'parts': [{'kind': 'text', 'text': 'hello'}],
                'messageId': uuid4().hex,
            },
            'metadata': {
                'stream': False  # explicitly specify not to use streaming mode
            }
        }
        
        simple_request = SendMessageRequest(
            id=str(uuid4()), 
            params=MessageSendParams(**simple_payload)
        )
        
        response = await client.send_message(simple_request)
        logger.info(f"simple mode response: {response.model_dump(mode='json', exclude_none=True)}")
        
        # test 2: streaming mode
        logger.info("\n" + "=" * 60)
        logger.info("test 2: streaming mode")
        logger.info("=" * 60)
        
        streaming_payload = {
            'message': {
                'role': 'user',
                'parts': [{'kind': 'text', 'text': 'hello with streaming mode'}],
                'messageId': uuid4().hex,
            }
        }
        
        streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()), 
            params=MessageSendParams(**streaming_payload)
        )
        
        logger.info("start streaming response...")
        stream_response = client.send_message_streaming(streaming_request)
        
        event_count = 0
        async for chunk in stream_response:
            event_count += 1
            logger.info(f"streaming event #{event_count}: {chunk.model_dump(mode='json', exclude_none=True)}")
        
        logger.info(f"streaming mode completed, received {event_count} events")
        
        # test 3: streaming mode
        logger.info("\n" + "=" * 60)
        logger.info("test 3: streaming mode")
        logger.info("=" * 60)
        
        config_streaming_payload = {
            'message': {
                'role': 'user',
                'parts': [{'kind': 'text', 'text': 'hello'}],
                'messageId': uuid4().hex,
            },
            'metadata': {
                'stream': True  # explicitly specify to use streaming mode
            }
        }
        
        config_streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()), 
            params=MessageSendParams(**config_streaming_payload)
        )
        
        logger.info("start config streaming response...")
        config_stream_response = client.send_message_streaming(config_streaming_request)
        
        config_event_count = 0
        async for chunk in config_stream_response:
            config_event_count += 1
            logger.info(f"config streaming event #{config_event_count}: {chunk.model_dump(mode='json', exclude_none=True)}")
        
        logger.info(f"config streaming mode completed, received {config_event_count} events")
        
        # test 4: simple mode
        logger.info("\n" + "=" * 60)
        logger.info("test 4: simple mode")
        logger.info("=" * 60)
        
        simple_streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()), 
            params=MessageSendParams(**simple_payload)
        )
        
        logger.info("start simple mode streaming response...")
        simple_stream_response = client.send_message_streaming(simple_streaming_request)
        
        simple_event_count = 0
        async for chunk in simple_stream_response:
            simple_event_count += 1
            logger.info(f"simple streaming event #{simple_event_count}: {chunk.model_dump(mode='json', exclude_none=True)}")
        
        logger.info(f"simple mode streaming completed, received {simple_event_count} events")

if __name__ == '__main__':
    asyncio.run(test_different_modes())
