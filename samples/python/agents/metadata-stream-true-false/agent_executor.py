from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from a2a.types import TaskStatusUpdateEvent, TaskStatus, TaskState
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Get a logger instance

# --8<-- [start:HelloWorldAgent]
class HelloWorldAgent:
    """Hello World Agent."""

    async def invoke(self) -> str:
        return 'Hello World'


# --8<-- [end:HelloWorldAgent]


# --8<-- [start:HelloWorldAgentExecutor_init]
class HelloWorldAgentExecutor(AgentExecutor):
    """Test AgentProxy Implementation."""

    def __init__(self):
        self.agent = HelloWorldAgent()

    # --8<-- [end:HelloWorldAgentExecutor_init]
    # --8<-- [start:HelloWorldAgentExecutor_execute]
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        # 检查配置，决定使用哪种处理策略
        use_streaming_mode = self._should_use_streaming_mode(context)
        
        if use_streaming_mode:
            # 流式模式：推送多个状态更新事件
            await self._execute_streaming_mode(context, event_queue)
        else:
            # 简单模式：直接返回结果
            await self._execute_simple_mode(context, event_queue)

    def _should_use_streaming_mode(self, context: RequestContext) -> bool:
        """判断是否应该使用流式模式"""
        # 方法：检查配置参数中的 stream 字段
        print('print context.configuration', context.configuration)
        print('print context.metadata', context.metadata)

        # 检查 MessageSendParams 的 metadata 字段
        if context.metadata and context.metadata.get('stream') == True:
            logger.info('Using streaming mode from MessageSendParams metadata')
            return True
        
        # 默认使用简单模式
        logger.info('Using simple mode')
        return False

    async def _execute_simple_mode(
        self, 
        context: RequestContext, 
        event_queue: EventQueue
    ) -> None:
        """简单模式：直接返回结果，不推送中间状态"""
        result = await self.agent.invoke()
        await event_queue.enqueue_event(new_agent_text_message(f"Simple result: {result}"))

    async def _execute_streaming_mode(
        self, 
        context: RequestContext, 
        event_queue: EventQueue
    ) -> None:
        """流式模式：推送多个状态更新事件"""
        # 模拟处理过程，推送多个状态更新事件
        status_update1 = TaskStatusUpdateEvent(
            task_id=context.task_id,
            context_id=context.context_id,
            status=TaskStatus(
                state=TaskState.working,
                message=new_agent_text_message("Starting to process...")
            ),
            final=False
        )
        await event_queue.enqueue_event(status_update1)
        await asyncio.sleep(0.5)  # 模拟处理时间
        
        status_update2 = TaskStatusUpdateEvent(
            task_id=context.task_id,
            context_id=context.context_id,
            status=TaskStatus(
                state=TaskState.working,
                message=new_agent_text_message("Processing your request...")
            ),
            final=False
        )
        await event_queue.enqueue_event(status_update2)
        await asyncio.sleep(0.5)  # 模拟处理时间
        
        result = await self.agent.invoke()
        # 最终结果使用 Message 事件
        await event_queue.enqueue_event(new_agent_text_message(f"Final result: {result}"))

    # --8<-- [end:HelloWorldAgentExecutor_execute]

    # --8<-- [start:HelloWorldAgentExecutor_cancel]
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

    # --8<-- [end:HelloWorldAgentExecutor_cancel]
