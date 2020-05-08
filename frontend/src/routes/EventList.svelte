<script>
  import * as api from "../api";
  import {onMount} from "svelte";
  import EventItem from "../components/EventItem.svelte";
  import {loggedIn, events} from '../store';
  import CreateEvent from "../components/CreateEvent.svelte";

  onMount(loadEvents);

  async function loadEvents() {
    let result = await api.listEvents();
    $events = result.results
  }

  function test() {
    alert("ebalal")
  }

</script>
<main>
  <h1>Recent events</h1>

  {#if $events}
  <ul>
  {#each $events as event }
      <li>
        <EventItem {event}  />
      </li>
  {/each}
  </ul>
<!--    {#if $loggedIn}-->
      <CreateEvent on:test={test} />
<!--    {/if}-->
  {:else}
  <p class="loading">loading...</p>
  {/if}
</main>

