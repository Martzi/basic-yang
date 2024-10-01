# YANG Extension

## YANG modules & features

### Custom YANG modules:
 - application-layer@2024-07-24.yang
 - network-layer@2024-07-24.yang
 - device-layer@2024-07-24.yang

### Required YANG modules:
 - ietf-inet-types@2013-07-15.yang
 - ietf-network@2018-02-26.yang
 - ietf-network-topology@2018-02-26.yang

## YANG validation from CLI:
```
yanglint -ii -t data -s -p src/yang-modules/application-layer@2024-07-24.yang src/yang-modules/network-layer@2024-07-24.yang src/yang-modules/device-layer@2024-07-24.yang src/yang-modules/ietf-network@2018-02-26.yang src/yang-modules/ietf-network-topology@2018-02-26.yang src/yang-modules/yang_content.xml
```

## Resulting YANG tree:
```
module: ietf-network
  +--rw networks
     +--rw network* [network-id]
        +--rw network-id            network-id
        +--rw network-types
        |  +--rw dl:device-layer-topology!
        |  +--rw nl:network-layer-topology!
        +--rw supporting-network* [network-ref]
        |  +--rw network-ref    -> /nw:networks/nw:network/nw:network-id
        +--rw node* [node-id]
        |  +--rw node-id                          node-id
        |  +--rw supporting-node* [network-ref node-ref]
        |  |  +--rw network-ref    -> ../../../nw:supporting-network/nw:network-ref
        |  |  +--rw node-ref       -> /nw:networks/nw:network/nw:node/nw:node-id
        |  +--rw dl:device-layer-node-attributes
        |  |  +--rw dl:device-name?   string
        |  |  +--rw dl:device-type?   string
        |  |  +--rw dl:weight?        string
        |  +--rw nt:termination-point* [tp-id]
        |  |  +--rw nt:tp-id                                         tp-id
        |  |  +--rw nt:supporting-termination-point* [network-ref node-ref tp-ref]
        |  |  |  +--rw nt:network-ref    -> ../../../nw:supporting-node/nw:network-ref
        |  |  |  +--rw nt:node-ref       -> ../../../nw:supporting-node/nw:node-ref
        |  |  |  +--rw nt:tp-ref         -> /nw:networks/nw:network[nw:network-id=current()/../network-ref]/nw:node[nw:node-id=current()/../node-ref]/termination-point/tp-id
        |  |  +--rw dl:device-layer-termination-point-attributes
        |  |  |  +--rw dl:port-name?           string
        |  |  |  +--rw dl:port-type?           string
        |  |  |  +--rw dl:wired?               string
        |  |  |  +--rw usb:version?             string
        |  |  |  +--rw usb:power-consumption?   decimal64
        |  |  +--rw nl:network-layer-termination-point-attributes
        |  |     +--rw nl:interface-name?     string
        |  |     +--rw nl:interface-type?     enumeration
        |  |     +--rw nl:interface-status?   enumeration
        |  |     +--rw nl:ip-address?         inet:ip-address
        |  |     +--rw nl:mac-address?        string
        |  +--rw nl:network-layer-node-attributes
        |     +--rw nl:node-name?   string
        |     +--rw nl:node-type?   enumeration
        +--rw nt:link* [link-id]
           +--rw nt:link-id                          link-id
           +--rw nt:source
           |  +--rw nt:source-node?   -> ../../../nw:node/nw:node-id
           |  +--rw nt:source-tp?     -> ../../../nw:node[nw:node-id=current()/../source-node]/termination-point/tp-id
           +--rw nt:destination
           |  +--rw nt:dest-node?   -> ../../../nw:node/nw:node-id
           |  +--rw nt:dest-tp?     -> ../../../nw:node[nw:node-id=current()/../dest-node]/termination-point/tp-id
           +--rw nt:supporting-link* [network-ref link-ref]
           |  +--rw nt:network-ref    -> ../../../nw:supporting-network/nw:network-ref
           |  +--rw nt:link-ref       -> /nw:networks/nw:network[nw:network-id=current()/../network-ref]/link/link-id
           +--rw dl:device-layer-link-attributes
           |  +--rw dl:physical-link-name?           string
           |  +--rw dl:physical-link-type?           string
           |  +--rw dl:cable-length?                 uint8
           |  +--rw usb:source-connector-type?        string
           |  +--rw usb:destination-connector-type?   string
           |  +--rw usb:max-data-transfer?            uint16
           |  +--rw usb:max-power-transfer?           uint16
           +--rw nl:network-layer-link-attributes
              +--rw nl:link-name?   string
              +--rw nl:link-type?   enumeration
              +--rw nl:_5qi?        uint8
              +--rw nl:gfbr?        uint8
              +--rw nl:mfbr?        uint8
              +--rw nl:pdb?         uint8
              +--rw nl:per?         uint8
```

## testing:

yang modulok hozzáadása:

add src/yang-modules/standard-modules/ietf-network-topology@2018-02-26.yang src/yang-modules/standard-modules/ietf-network@2018-02-26.yang src/yang-modules/standard-modules/ietf-inet-types@2013-07-15.yang src/yang-modules/interfaces/ethernet-port.yang src/yang-modules/interfaces/usb-port.yang src/yang-modules/topology/device-layer@2024-09-10.yang src/yang-modules/topology/network-layer@2024-07-24.yang

validálás yanglint cli-ből:  data -t data src/yang-modules/instance-data3.xml 