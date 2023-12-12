

Porthouse is designed to be agnostic and as transparent as possible.
It's fashioned to be used for any general _realtime_ communication method, over local or long distance.

The aim is to reduce the overhead of writing a realtime solution. Many occasions I've thought _"Hmm, I could really do with an un-opinionated realtime backend"_ without writing a _solution_.

Indeed a vast array of choices and solutions exist; many frontend libs such as fastapi, flask, and _websockets_ all have _server solutions_. In that I pick the base product and then fashion around it.

With starlette I can create great solutions - but then extending those solutions require more framework. Then to _adapt_ that framework, I found myself copy/pasting ideas through each project.

Sometimes I need a local broadcast (easy right), then I need pub/sub rooms (cool enough...). Then I want QR verification .. great - but in a channel automated key channel (okay.. fair enough). Then I want to drop it on a server and use it (.. ooh okay. More work).

Finally it comes to use - and I want to _bridge_ nodes, make clusters. _Hmm_ I hear you say. That's when this became a whole new solution. Let's start again.


## The goal

The concept should be as easy as writing a django or fastapi application - but for realtime sockets.
The _outof the box_ solution has enough components to write a wholesome solution quickly, without worrying about the middle management.

The dream is _function in_, _function out_ for socket to socket; both transparent and wrapped. Allowing a developer to produce _raw_ local toys - or utilise the base for larger projects.

### Function in Function Out - FiFo

The Function in Function Out (FiFo) mantra dictates the preference to output. The message through A, should be explicit at B; no inference. Therefore a developer can easily ascertain the core functionality.

On the surface `porthouse` aims to be agnostic to requirements, connected by anything, with many interfaces for protocols.

> Fundamentally porthouse is a _message routing_ tool, of which also has http an websockets plugs.


## Target Projects:

+ Agent Programming
+ Internal IoT
+ Doorbell
+ VOL graph stepper machine and mesh coms
+ Sunvox API
+ audio streaming toys
+ long distance graph editing
+ Website tool management (file uploads, user chats etc.)
+ multi user file editor (training students.)
+ sms gateway
    thtough api or android
+ file list aggregations across devices
+ system to system audio stream
    I have no clue how to do this, it'll be fun to find out.
+ remote keyboard mouse
+ VLC remote and other remote controls (prkeyboard)

## Marketplace.

A tooling to install and use community driven addons; such as agent toys or ping testing.
They should be installed with structured parameters, such that automated testing can evaluate how the module
intergrates. Given a tight enough solution - these addon modules can be tested in the same method as the entire suite; for both developer _code coverage_ awareness, and future porthouse (system) upgrades.


### IoT

Building a house of interconnected things is great - but I want it in-house, no fuss, no magic, or _docker_ or 10 tool configuration. A Simple "run this" on a Raspberry Pi Zero.

+ Internal (House) IoT coms; device-to-device with a central router
    + Door bell: Pop messages, with long distance securities, file dropping, multi channel events.


---

+ sunvox audio channels
+ graph to graph (long distance) bridging


### External to internal messaging tools

An internal mesh, connected to an external mesh, both with unique securities, managed by one owner through one permission system. (Bridging)


### personal 2factor management

building safe long-distance security solutions are tricky when managing the architecture and logic. Porthouse allows the complete offset of node to node management (aka _channel locking_) through authentication flows.

Coupled with the sequences engine (Another project) we can perform many step verification processes over the wire - without complex caching processes.


### Self Agency Toys

Working with Braitenberg vehicles is great fun; but attempting to plug many _units_ into tidy threads is a hassle; porthouse deletes this problem by allowing socket messaging out the box for offloading complex calculations to another part of a system.

### Graph Theory

Much of my own study is graph theory (nodes and edges  - spots and lines).
A realtime plug-and-play messaging system, allowing the developer to fire agnostic events across a distributed graph. Each node may be connected to an ID or to a remote graph, providing the ability to easily _pluck_ at edges and nodes without building a framework of interaction for your graph


### Free open source real-time messaging

I very much believe in personal security and freedom. With this is the necessity to own personal communications. This porthouse project is a step towards information liberty, removing the mandate for online realtime systems