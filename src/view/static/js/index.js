const URL = "127.0.0.1"
    , PORT = window.location.port
    , TOKEN = 1111
    ;


const makeUrl = function(client_id) {
    return `ws://${URL}:${PORT}/${TOKEN}`
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

    isOpen = false
    onopen() {
        let m = `${this._id} onopen`
        const args = Array.from(arguments)
        this.isOpen = true
        console.log(m, args)
    }

    onmessage(e) {
        let m = `${this._id} onmessage`
        const args = Array.from(arguments)

        console.log(m, e.data)
    }

    onerror() {
        let m = `${this._id} onerror`
        const args = Array.from(arguments)
        console.log(m, args)
    }

    onclose() {
        let m = `${this._id} onclose`
        this.isOpen = false
        const args = Array.from(arguments)
        console.log(m, args)
    }

    sendBytes(count=17, fill=42) {
        let byteArray = new Uint8Array(count);
        byteArray.fill(fill);
        return this.send(byteArray.buffer);
    }
}

class MultiSocket {
    /* Manage many sockets */

    generate(count) {
        this.sockets = generateMany(count)
    }

    each(f) {
        this.sockets.forEach(f)
    }

    send(t) {
        this.each((w)=> w.send(t))
    }

    close() {
        this.each(x=>x.close())
    }

    openCount() {
        let c = 0
        this.sockets.forEach(s=>c += s.isOpen)
        return c
    }

    static create(count) {
        const r = new MultiSocket
        r.generate(count)
        return r
    }
}



var client_id = Date.now()

var newSocket = function(client_id){
    const url = makeUrl(client_id)
    var ws = new PocketSocket.connect(url);

    return ws
}

const pump = function(count=9, create=30){
    for (var i = 0; i < count; i++) {
        let v = MultiSocket.create(create)
        setTimeout(function(){
            this.multiSocket.close()
        }.bind({multiSocket:v}), 3000)
    }
}

var emitEvent = function(event) {
    events.emit('socket-message', event)
}


var send = function(text) {
    ws.send(text)
}


var generateMany = function(count=5) {
    const r = []
    for (var i = 0; i < count; i++) {
        let url = makeUrl(i)
        let w = PocketSocket.connect(url)
        w._id = i
        r.push(w)
    }
    return r
}