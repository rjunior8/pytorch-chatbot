from aiohttp import web
import asyncio
import jinja2
import aiohttp_jinja2
import os
import socketio

from chat import proc_msg


sio = socketio.AsyncServer(async_mode='aiohttp', async_handlers=True)
app = web.Application()
sio.attach(app)

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)

async def chat(request):
    response = aiohttp_jinja2.render_template("chat.html", request, context={})
    return response

@sio.on('send_msg', namespace="/bot_chat")
async def bot_chat(sid, data):
    bot_name, reply = proc_msg(sentence=data)
    await sio.emit('reply', {"user": bot_name, "msg": reply}, room=sid, namespace='/bot_chat')


app.add_routes([web.get('/', chat),])


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)