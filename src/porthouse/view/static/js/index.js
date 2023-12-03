/*

    p = PocketSocket.commander(TOKEN)
    m = MultiSocket.create(3);
 */

const DOMAIN = "127.0.0.1"
    , PORT = window.location.port
    , URL = ""
    , COMMAND_URL = "/commander"
    , TOKEN = '2bee8693-76a1-474a-8088-86447018ce73'
    ;


const makeUrl = function(domain=DOMAIN, url=URL, token=TOKEN) {
    return `ws://${domain}:${PORT}${url}/${token}`
}

let _c = 0;

class PocketSocket extends WebSocket {
    static commander(token) {
        let s = PocketSocket.connect(COMMAND_URL, token)
        s._id = ++_c;
        return s
    }

    static connect(url, _token) {
        let u = url
        if(_token !== undefined) {
            u = makeUrl(DOMAIN, url, _token)
        }
        const w = new PocketSocket(u)

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

    sendJSON(obj) {
        this.send(JSON.stringify(obj))
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

var newSocket = function(client_id, token=TOKEN){
    const url = makeUrl(client_id, token)
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
        let w = PocketSocket.connect(URL, TOKEN)
        w._id = i
        r.push(w)
    }
    return r
}