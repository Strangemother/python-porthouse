const URL = "127.0.0.1"
    , PORT = 9004
    ;


const makeUrl = function(client_id) {
    return `ws://${URL}:${PORT}/${client_id}`
}


class PocketSocket extends WebSocket {

    static connect(url) {
        const w = new PocketSocket(url)

        w.addEventListener("error", w.onerror.bind(w));
        w.addEventListener("message", w.onmessage.bind(w));
        w.addEventListener("close", w.onclose.bind(w));
        w.addEventListener("open", w.onopen.bind(w));

        return w
    }

    onopen() {
        console.log('onopen', arguments)
    }

    onmessage() {
        console.log('onmessage', arguments)
    }

    onerror() {
        console.log('onerror', arguments)
    }

    onclose() {
        console.log('onclose', arguments)
    }

    sendBytes(count=17, fill=42) {
        let byteArray = new Uint8Array(count);
        byteArray.fill(fill);
        return this.send(byteArray.buffer);
    }
}

var client_id = Date.now()


var newSocket = function(client_id){
    const url = makeUrl(client_id)
    var ws = new PocketSocket.connect(url);

    return ws
}

var emitEvent = function(event) {
    events.emit('socket-message', event)
}

var send = function(text) {
    ws.send(text)
}
