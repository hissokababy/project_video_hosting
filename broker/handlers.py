from broker.confings import rabbit
from video_hosting.validators import ValidateMessage
from video_hosting.services.user import VideoHostingService


rabbit.create_exchange(exchange='video_hosting_exchange', exchange_type='direct')


@rabbit.message_handler(queue='user_queue', auto_ack=True, queue_exchange='video_hosting_exchange', 
                        queue_routing_key='user')
def user_activity_handler(ch, method, properties, body):
    service = VideoHostingService()
    message = ValidateMessage.validate_user_id(body)

    service.change_user(message.id, message.active)
