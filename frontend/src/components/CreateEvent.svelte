<script>
  import * as api from "../api";
  import { createEventDispatcher } from 'svelte';
  import {events} from "../store"
  
  export let event = getEmptyEvent();
  let errors = {};

  function getEmptyEvent() {
    return {
      id: null,
      title: '',
      description: '',
      date_start: ''
    }
  }

  async function saveEvent() {
    let result;
    if (event.id === null) {
      result = await api.createEvent(event);
    } else {
      result = await api.updateEvent(event);
    }

    let msg = await result.json();

    if (result.status === 201 || result.status === 200) {
      result = msg;
      errors = {};

      // store magic
      let evs = $events;
      evs.push(result);
      $events = evs;

      event = getEmptyEvent();
    } else {
      errors = msg;
    }
  }
  
</script>


<div>
  <h2>Create new event</h2>

  <label> Title <input bind:value={event.title} placeholder="title"></label>
  <label> Description <input bind:value={event.description} placeholder="description"></label>
  <label> Date <input bind:value={event.date_start} placeholder="2020-12-31 18:00"></label>

  <button on:click={saveEvent}>{#if event.id === null}Create{:else}Update{/if}</button>
    {#if Object.keys(errors).length > 0}
      <ul class="errors">
        {#each Object.keys(errors) as field}
          <li>{field}: {errors[field]}</li>
        {/each}
      </ul>
    {/if}
</div>
