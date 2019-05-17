/* eslint-env node */
module.exports = class Model {
  constructor() {
    this.store = {rooms: [], persons: [], topics: []}
    this.listeners = {}
  }

  registerListener(listener) {
    const id = Math.max(...Object.keys(this.listeners), 0) + 1
    this.listeners[id] = listener
    return id
  }

  unregisterListener(listenerId) {
    delete this.listeners[listenerId]
  }

  notifyListeners(change) {
    Object.values(this.listeners).forEach(listener => listener(change))
  }

  async getAll() {
    const nodes = [
      ...this.store.rooms,
      ...this.store.persons,
      ...this.store.topics
    ]
    if (nodes.length === 0) {
      return {nodes: [{id: -1, name: 'No data existing yet'}]}
    }
    return {nodes}
  }

  getById(type, id) {
    return this.store[type + 's'][id]
  }

  find(type, node) {
    return this.store[type + 's'].find(n => n.id === node.id || (!node.id && n.name === node.name))
  }

  addNode(type, node) {
    if (this.store.rooms.length + this.store.persons.length + this.store.topics.length === 0) {
      this.notifyListeners({type: 'deleteNode', node: {id: -1}})
    }
    const existing = this.find(type, node)
    if (existing) {
      existing.weight = Math.sqrt(existing.weight * existing.weight + node.weight)
      this.notifyListeners({type: 'changeNode', node: existing})
      return existing.id
    } else {
      if (!node.id) {
        node.id = type + '_' + node.name
      }
      node.weight = Math.sqrt(node.weight || 1)
      this.store[type + 's'].push(node)
      this.notifyListeners({type: 'addNode', node})
      return node.id
    }
  }

  changeNode(id, type, change) {
    this.notifyListeners({type: 'changeNode', node: change})
  }

  addLink(node1, node2) {
    const type = node2.className + 's'
    node1.links = node1.links || {}
    node1.links[type] = node1.links[type] || []
    node1.links[type].push(node2.id)
    this.notifyListeners({type: 'addLink', source: node1.id, target: node2.id})
    return node2.id
  }
}
