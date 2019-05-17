/* eslint-env node */

const faker = require('faker')

const names = {}
let sequence = 1

module.exports = ({model}) => {
  return {
    addRoom(data) {
      const topics = data.topics || []
      delete data.topics
      const persons = data.users || []
      delete data.users
      data.className = 'room'
      data.id = data.id || 'room_' + sequence++
      data.weight = 1
      model.addNode('room', data)

      data.links = {}
      data.links.topics = topics.map(prepareTopic)
      data.links.persons = persons.map(preparePerson)
      model.changeNode(data.id, 'rooms', data)
      return {ok: true}

      function prepareTopic(topic) {
        const existing = model.find('topic', topic)
        if (!existing) {
          topic.className = 'topic'
          model.addNode('topic', topic)
          topic.id = topic.id || 'topic_' + sequence++
        }
        data.weight = Math.sqrt(data.weight * data.weight + topic.weight)
        return model.addLink(data, existing || topic)
      }

      function preparePerson(name) {
        const person = names[name] || {className: 'person', weight: 1, name: faker.name.findName()}
        if (!person.id) {
          person.id = person.id || 'person_' + sequence++
          model.addNode('person', person)
        }
        names[name] = person
        return model.addLink(data, person)
      }
    }
  }
}