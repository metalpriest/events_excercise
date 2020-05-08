<script>
  import * as api from "../api";
  import { createEventDispatcher } from 'svelte';
  import {events} from "../store"
  
  export let event = getEmptyEvent();

  function getEmptyEvent() {
    return {
      id: null,
      title: '',
      description: '',
      date_start: ''
    }
  }

  async function saveEvent() {
    let result = await api.createEvent(event);
    debugger;
    if (result.status === 200) {
      result = await result.json();
      let events = $events;
      debugger;
      events.append(result);
      $events = events;

      event = getEmptyEvent();
    }
  }
  
</script>


<div>
  <h2>Create new event</h2>

  <label> Title <input bind:value={event.title} placeholder="title"></label>
  <label> Description <input bind:value={event.description} placeholder="description"></label>
  <label> Date <input bind:value={event.date_start} placeholder="2020-12-31 18:00"></label>

  <button on:click={saveEvent}>{#if event.id === null}Create{:else}Update{/if}</button>
</div>
