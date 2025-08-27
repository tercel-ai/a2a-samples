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
    """测试不同的处理模式"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    base_url = 'http://localhost:9999'

    async with httpx.AsyncClient() as httpx_client:
        # 获取 agent card
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
        agent_card = await resolver.get_agent_card()
        
        # 创建客户端
        client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)
        
        # 测试1：普通消息（应该使用简单模式）
        logger.info("=" * 60)
        logger.info("测试1：普通消息（简单模式）")
        logger.info("=" * 60)
        
        simple_payload = {
            'message': {
                'role': 'user',
                'parts': [{'kind': 'text', 'text': 'hello'}],
                'messageId': uuid4().hex,
            },
            'metadata': {
                'stream': False  # 明确指定不使用流式模式
            }
        }
        
        simple_request = SendMessageRequest(
            id=str(uuid4()), 
            params=MessageSendParams(**simple_payload)
        )
        
        response = await client.send_message(simple_request)
        logger.info(f"简单模式响应: {response.model_dump(mode='json', exclude_none=True)}")
        
        # 测试2：包含 streaming 关键词的消息（应该使用流式模式）
        logger.info("\n" + "=" * 60)
        logger.info("测试2：包含 streaming 关键词的消息（流式模式）")
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
        
        logger.info("开始流式响应...")
        stream_response = client.send_message_streaming(streaming_request)
        
        event_count = 0
        async for chunk in stream_response:
            event_count += 1
            logger.info(f"流式事件 #{event_count}: {chunk.model_dump(mode='json', exclude_none=True)}")
        
        logger.info(f"流式模式完成，总共收到 {event_count} 个事件")
        
        # 测试3：通过 metadata.stream=True 指定流式模式
        logger.info("\n" + "=" * 60)
        logger.info("测试3：通过 metadata.stream=True 指定流式模式")
        logger.info("=" * 60)
        
        config_streaming_payload = {
            'message': {
                'role': 'user',
                'parts': [{'kind': 'text', 'text': 'hello'}],
                'messageId': uuid4().hex,
            },
            'metadata': {
                'stream': True  # 明确指定使用流式模式
            }
        }
        
        config_streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()), 
            params=MessageSendParams(**config_streaming_payload)
        )
        
        logger.info("开始配置流式响应...")
        config_stream_response = client.send_message_streaming(config_streaming_request)
        
        config_event_count = 0
        async for chunk in config_stream_response:
            config_event_count += 1
            logger.info(f"配置流式事件 #{config_event_count}: {chunk.model_dump(mode='json', exclude_none=True)}")
        
        logger.info(f"配置流式模式完成，总共收到 {config_event_count} 个事件")
        
        # 测试4：普通消息的流式请求（应该使用简单模式）
        logger.info("\n" + "=" * 60)
        logger.info("测试4：普通消息的流式请求（简单模式）")
        logger.info("=" * 60)
        
        simple_streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()), 
            params=MessageSendParams(**simple_payload)
        )
        
        logger.info("开始简单模式的流式响应...")
        simple_stream_response = client.send_message_streaming(simple_streaming_request)
        
        simple_event_count = 0
        async for chunk in simple_stream_response:
            simple_event_count += 1
            logger.info(f"简单流式事件 #{simple_event_count}: {chunk.model_dump(mode='json', exclude_none=True)}")
        
        logger.info(f"简单模式流式完成，总共收到 {simple_event_count} 个事件")

if __name__ == '__main__':
    asyncio.run(test_different_modes())
