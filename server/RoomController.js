/* eslint-env node */

const faker = require('faker')

const names = {}
let nameId = 1

module.exports = ({model}) => {
  return {
    addRoom(data) {
      const topics = data.topics || []
      delete data.topics
      const persons = data.users || []
      delete data.users
      data.className = 'room'
      model.addNode('room', data)

      data.links = {}
      data.links.topics = topics.map(prepareTopic)
      data.links.persons = persons.map(preparePerson)
      data.weight = (data.links.topics && Math.log(data.links.topics.length + 1)) || 1
      model.changeNode(data.id, 'rooms', data)
      return {ok: true}

      function prepareTopic(topic) {
        const existing = model.find('topic', topic)
        if (!existing) {
          topic.className = 'topic'
          model.addNode('topic', topic)
        }
        return model.addLink(data, existing || topic)
      }

      function preparePerson(name) {
        if (!names[name]) {
          names[name] = {id: 'person_' + nameId++, name: faker.name.findName()}
        }
        const person = Object.assign({className: 'person', weight: 1}, names[name])
        const existing = model.getById('person', names[name].id)
        if (!existing) {
          model.addNode('person', person)
        }
        return model.addLink(data, person)
      }
    }
  }
}