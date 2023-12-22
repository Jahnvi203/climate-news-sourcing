<template>
  <div class="card-body">
    <i
      class="d-flex justify-content-center font-weight-bold"
      style="text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.2)"
      >{{
        stage == "search"
          ? "Retrieving Articles ..."
          : stage == "topic"
          ? "Classifying Articles ..."
          : stage.includes == "analysing_article"
          ? "Analysing Article ..."
          : stage == "analysing_article_senti"
          ? "Analysing Article ..."
          : stage == "analysing_article_summ"
          ? "Analysing Article ..."
          : stage == "analysing_article_topic"
          ? "Analysing Article ..."
          : "Loading ..."
      }}</i
    >
    <i
      style="font-size: 14px"
      class="d-flex justify-content-center mb-3"
      v-if="stage == 'analysing_article_senti'"
      >Calculating Sentiments</i
    >
    <i
      style="font-size: 14px"
      class="d-flex justify-content-center mb-3"
      v-if="stage == 'analysing_article_summ'"
      >Generating Summaries</i
    >
    <i
      style="font-size: 14px"
      class="d-flex justify-content-center mb-3"
      v-if="stage == 'analysing_article_topic'"
      >Looking for Topics</i
    >
    <h5
      class="card-title mb-3"
      v-if="
        stage == 'search' ||
        stage == 'topic' ||
        stage == 'analysing_article' ||
        stage == 'analysing_article_summ' ||
        stage == 'analysing_article_topic'
      "
    >
      <div class="page-loader my-3">
        <img
          src="../../../../src/assets/loading-gif.gif"
          style="width: 5%; height: auto"
        />
        <!-- <div class="cube"></div>
        <div class="cube"></div>
        <div class="cube"></div>
        <div class="cube"></div> -->
      </div>
    </h5>
    <h5 class="card-title" v-else-if="stage == 'analysing_article_senti'">
      <loading-sentiments />
    </h5>
  </div>
</template>

<script>
import LoadingSentiments from "./LoadingSentiments";

export default {
  components: {
    LoadingSentiments,
  },
  name: "LoadingTopics",
  props: {
    stage: {
      type: String,
    },
  },
};
</script>

<style lang="scss" scoped>
$colors: #f5f5f5, #f0f0f0, #e7e7e7, #dadada;
.page-loader {
  display: flex;
  justify-content: center;
  align-items: center;

  width: 100%;
  height: 100%;
  //   background-color: #333;
  z-index: 999;
}
.cube {
  width: 40px;
  height: 40px;
  margin-right: 10px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.486);
  @for $index from 1 through length($colors) {
    &:nth-child(#{$index}) {
      background-color: nth($colors, $index);
    }
  }

  //   Only apply first action to the first cube, most left cube
  &:first-child {
    animation: left 1s infinite;
  }
  &:last-child {
    animation: right 1s infinite 0.5s;
  }

  @keyframes left {
    40% {
      transform: translateX(-60px);
    }
    50% {
      transform: translateX(0);
    }
  }
  @keyframes right {
    40% {
      transform: translateX(60px);
    }
    50% {
      transform: translateX(0);
    }
  }
}
</style>
