<script>
  import { onMount } from "svelte";
  import GuessCode from "./lib/GuessCode.svelte";
  let codes = [];
  let langs = [];
  let i = 0;

  onMount(async () => {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/randoms`);
    codes = await res.json();
    const langs_res = await fetch(`${import.meta.env.VITE_API_URL}/api/langs`);
    langs = await langs_res.json();
  });
</script>

<main>
  <h1>What programming language is this??</h1>
  {#if codes.length > 0 && langs.length > 0}
    <GuessCode {codes} {langs} />
  {:else}
    <h2>Loading...</h2>
  {/if}
</main>

<style>
  main {
    position: relative;
    margin: 0 auto;
    padding: 0ch 2ch 2ch 2ch;
    max-width: 88ch;
    min-height: 80vh;
  }
</style>
