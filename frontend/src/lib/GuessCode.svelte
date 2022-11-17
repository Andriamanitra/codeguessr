<script>
  import { fade } from "svelte/transition";

  export let codes;
  export let langs;
  export let numOptions = 8;
  let i = 0;
  let score = 0;
  let correctnessMsg = "";
  let shownLangs = randomizedOptions(numOptions);
  let visible = false;
  function randomizedOptions(n) {
    let langOptions = [codes[i].language];
    while (langOptions.length < n) {
      let randomIndex = Math.floor(Math.random() * langs.length);
      let randomLang = langs[randomIndex];
      if (!langOptions.includes(randomLang)) {
        langOptions.push(randomLang);
      }
    }
    return langOptions.sort();
  }

  function censored_code(obj) {
    if (obj.language.length > 3) {
      let langNameRegex = new RegExp(obj.language, "gi");
      return obj.code.replaceAll(langNameRegex, "PROGRAMMING_LANGUAGE_NAME");
    } else {
      return obj.code;
    }
  }

  async function pick(guess) {
    let correctLang = codes[i].language;
    if (guess === correctLang) {
      score += 1;
      correctnessMsg = "Correct!";
    } else {
      correctnessMsg = `WRONG! That was ${correctLang}!`;
    }
    visible = true;
    setTimeout(() => {
      visible = false;
    }, 500);
    i += 1;
    shownLangs = i < codes.length ? randomizedOptions(numOptions) : [];
  }
</script>

{#if i >= codes.length}
  <p class="results">
    You got {score} out of {i} correct.
    {#if score / i > 0.9}
      Excellent!
    {:else if score / i > 0.5}
      Not bad!
    {:else if score / i > 0.2}
      Not great...
    {:else}
      You suck at this!
    {/if}
  </p>
  <h2>Here's another look at the questions you had:</h2>
  {#each codes as code, idx}
    <h3>
      Question {idx + 1}: <a href={code.task_url}>{code.task_name}</a> - {code.language}
      <span class="solution-link">
        (<a
          href="{import.meta.env.VITE_API_URL}/api/solution/{code.solution_id}"
          >#{code.solution_id}</a
        >)</span
      >
    </h3>
    <pre class="code small">{code.code}</pre>
  {/each}
{:else}
  <h2>Task: {codes[i].task_name}</h2>
  <a href={codes[i].task_url}>View on Rosetta code (spoilers!)</a>
  <pre class="code">{censored_code(codes[i])}</pre>
  <div class="buttons flex">
    {#each shownLangs as lang}
      <button on:click={() => pick(lang)}>{lang}</button>
    {/each}
  </div>
{/if}
{#if visible}
  <div class="correct" out:fade={{ duration: 1000 }}>{correctnessMsg}</div>
{/if}

<style>
  .correct {
    font-size: 4em;
    position: fixed;
    top: 20vh;
    left: 0px;
    width: 100%;
    text-align: center;
  }
  .results {
    font-size: 2em;
    color: black;
    border: 5px solid black;
    border-radius: 20px;
    padding: 1ch;
    margin: 2ch;
  }
  h2,
  h3 {
    margin-right: 1ch;
    margin-bottom: 0px;
  }
  .code {
    border: 1px solid grey;
    padding: 5px;
    height: 30em;
    overflow-y: auto;
  }
  .small {
    height: 10em;
  }
  .solution-link {
    font-weight: lighter;
  }
  .flex {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    row-gap: 10px;
  }
  button {
    font-size: 1.1em;
    min-width: 18ch;
    padding: 5px;
    cursor: pointer;
  }
</style>
