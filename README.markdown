# pykey

## interface

### Server

you can start server simply with `python -m pykey.run`,
for more information type `python -m pykey.run -h`

### Client

there is no client in pykey, Instead you can connect server through telnet
type `$ telnet your-host your-port`

### Syntax

pykey use [bendy][bendy-repo] syntax, and there is 7 command. 

#### Data I/O 

To set value:

    (set! 'key' 'value')

`'key'` is should be string, `'value'` can be string or integer, and there is limit length in both `'key'` and `'value'`.

To remove value:

    (del 'key')

remove key/value from disk or memory. if there is no correspend key raise exception.

To get value:

    (get 'key')

get value from key, if there is no correspend key raise exception.

#### Data Handling with object

when you deal with data, you want know the information about datas.
For instance, is this really saved in disk? or if i redo command, what i get?.
In this situation, you can use simply `logging` function. 

    (logging 'object')

This is type of `object` below you can use. 

 - cache
 - store
 - query

#### Disk I/O

pykey don't write data into disk everytime you send command to server. so maybe you can want write, when you want. or you want set back your data before you send command. these command below is about this kind of sutff.

    query?

View set/del log to save or set back data 

    sav!

Save data in query log, this allow you to save data in disk when you want.
    
    redo

Set back data to one step before 

## developer

 - email: admire9 (at) gmail (dot) kr
 - website: [admire.kr](http://admire.kr)

[bendy-repo]: http://bitbucket.org/admire93/bendy
