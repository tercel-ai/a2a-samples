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
        # check configuration, decide which mode to use
        use_streaming_mode = self._should_use_streaming_mode(context)
        
        if use_streaming_mode:
            # streaming mode: push multiple status update events
            await self._execute_streaming_mode(context, event_queue)
        else:
            # simple mode: return result directly
            await self._execute_simple_mode(context, event_queue)

    def _should_use_streaming_mode(self, context: RequestContext) -> bool:
        """check if should use streaming mode"""
        # check stream field in configuration
        print('print context.configuration', context.configuration)
        print('print context.metadata', context.metadata)

        # check MessageSendParams metadata field
        if context.metadata and context.metadata.get('stream') == True:
            logger.info('Using streaming mode from MessageSendParams metadata')
            return True
        
        # default to simple mode
        logger.info('Using simple mode')
        return False

    async def _execute_simple_mode(
        self, 
        context: RequestContext, 
        event_queue: EventQueue
    ) -> None:
        """simple mode: return result directly, no intermediate status updates"""
        result = await self.agent.invoke()
        await event_queue.enqueue_event(new_agent_text_message(f"Simple result: {result}"))

    async def _execute_streaming_mode(
        self, 
        context: RequestContext, 
        event_queue: EventQueue
    ) -> None:
        """streaming mode: push multiple status update events"""
        # simulate processing, push multiple status update events
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
        await asyncio.sleep(0.5)  # simulate processing time
        
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
        await asyncio.sleep(0.5)  # simulate processing time
        
        result = await self.agent.invoke()
        # final result use Message event
        await event_queue.enqueue_event(new_agent_text_message(f"Final result: {result}"))

    # --8<-- [end:HelloWorldAgentExecutor_execute]

    # --8<-- [start:HelloWorldAgentExecutor_cancel]
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

    # --8<-- [end:HelloWorldAgentExecutor_cancel]
