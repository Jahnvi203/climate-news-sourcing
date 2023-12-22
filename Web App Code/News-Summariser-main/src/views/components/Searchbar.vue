<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Climate News</a>
    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarNavAltMarkup"
      aria-controls="navbarNavAltMarkup"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
      <div class="navbar-nav">
        <a class="nav-item nav-link active" href="/"
          >Home <span class="sr-only">(current)</span></a
        >
        <a class="nav-item nav-link" href="/entity">Charts</a>
      </div>
    </div>
  </nav>
  <div class="mt-5">
    <div class="card mb-4 px-1">
      <div class="px-4 py-4">
        <div>
          <!-- New Search Start -->
          <div class="col-lg-10 d-flex flex-column">
            <h5 class="font-weight-bold my-2">Select Source</h5>
            <div class="row">
              <div class="row my-2">
                <div class="callout" style="font-size: smaller">
                  View news articles from (CNN / BBC):
                </div>
                <form role="form" id="company-form" autocomplete="off">
                  <v-select
                    :options="companies"
                    label="company_name"
                    style="font-size: smaller; --vs-border-radius: 6px"
                    v-model="selected_source"
                  >
                  </v-select>
                </form>
              </div>
              <div class="row d-flex">
                <div class="callout" style="font-size: smaller">
                  Search by keywords:
                </div>
                <div class="col-9 mb-3">
                  <input
                    id="advanced_search_option_input"
                    v-model="keyword_to_search"
                    type="text"
                    class="form-control"
                    placeholder="Insert Query"
                    aria-label="old query"
                    aria-describedby="basic-addon1"
                    ref="advancedSearchOptionInput"
                  />
                </div>
              </div>

              <div>
                <span>
                  <button
                    type="submit"
                    class="btn bg-gradient-custom"
                    :disabled="isLoading"
                    @click="get_articles()"
                  >
                    Search
                  </button>
                </span>
              </div>
            </div>
          </div>
          <!-- News Search End -->
        </div>

        <!-- search bar content-->
      </div>
    </div>

    <!--ARTICLES RETURNED CARD-->
    <div class="card mb-4 px-1" v-if="searched">
      <div class="card-body px-4 py-4">
        <div v-if="isLoading" class="d-flex justify-content-center">
          <!-- <div class="spinner-grow" role="status">
            <span class="visually-hidden">Loading...</span>
          </div> -->
          <loading-topics :stage="stageOfSearch" />
        </div>
        <div v-else-if="query_results.length == 0 && !isLoading">
          <b class="site">No Results Found: </b>
          <hr />
        </div>

        <div v-else>
          <h4 class="fw-bolder text-center">
            Search Results for {{ selected_source }}
            <p class="text-s fst-italic site mb-1">
              (Returned {{ query_results.length }} results)
            </p>
          </h4>
          <div class="row">
            <div class="pb-2 col-6" id="sentiment_filter">
              <div class="callout" style="font-size: smaller">
                Sort Articles by
              </div>
              <form role="form" id="company-form" autocomplete="off">
                <select
                  class="form-control"
                  name="sentiment_to_filter_by"
                  id="sentiment_to_filter_by"
                  placeholder="Sort Articles by"
                  @change="filterMaster($event)"
                >
                  <option value="all">Show All</option>
                  <option value="dateMostRecent">
                    Date published: Most Recent
                  </option>
                  <option value="dateLeastRecent">
                    Date published: Least Recent
                  </option>
                  <option value="articleLengthLongest">
                    Article Length: Longest
                  </option>
                  <option value="articleLengthShortest">
                    Article Length: Shortest
                  </option>
                </select>
              </form>
            </div>
          </div>

          <hr />
          <br />

          <div class="row">
            <div
              class="row pb-3"
              v-for="(article, index) in current_page_results"
              :key="article.article_url + index"
            >
              <div class="col-10">
                <a
                  :href="article.article_url"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <h5>
                    {{ current_page * results_per_page + index + 1 }}.
                    {{ article.headline }}
                  </h5>
                </a>

                <p class="article_description mb-2">
                  Source: {{ article.source.replace("_", " ").toUpperCase() }}
                </p>

                <button
                  type="button"
                  data-bs-toggle="modal"
                  data-bs-target=".bd-example-modal-xl"
                  class="btn btn-sm btn-secondary"
                  @click="show_article(article)"
                >
                  View Article Details
                </button>
              </div>
              <div class="col-2">
                <div class="row text-end mt-2">
                  <div class="text-xs mb-2">
                    <div class="article_date_published">
                      Date Published: {{ article.date_published }}
                    </div>
                    <div class="article_date_published">
                      Article Length: {{ article.article_length }} words.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="query_results.length != 0 && !isLoading"
        class="card-footer mx-auto"
      >
        <div
          class="row"
          v-if="query_results_chunks && query_results_chunks.length > 0"
        >
          <!-- IF ONLY 5 or less pages -->
          <div v-if="query_results_chunks && query_results_chunks.length <= 5">
            <soft-pagination size="sm" color="dark">
              <soft-pagination-item prev @click="prevPage()" />
              <soft-pagination-item
                v-for="(each_chunk, index) in query_results_chunks"
                :key="index"
                :label="(index + 1).toString()"
                @click="showPage(index)"
                :active="curr_page_checker(index)"
              />
              <soft-pagination-item next @click="nextPage()" />
            </soft-pagination>
          </div>
          <!-- ELSE apply special pagination -->
          <div v-else>
            <!-- MID - SHOW FIRST PAGE...MIDDLE PAGES...LAST PAGE -->
            <div
              v-if="
                current_page >= 5 &&
                current_page <= query_results_chunks.length - 7
              "
            >
              <!-- <b>MID</b> -->
              <soft-pagination size="sm" color="dark">
                <soft-pagination-item prev @click="prevPage()" />
                <!-- FIRST PAGE -->
                <soft-pagination-item
                  :key="'0'"
                  :label="'1'"
                  @click="showPage('0')"
                  :active="curr_page_checker('0')"
                />
                &nbsp; ... &nbsp;
                <!-- CURRENT PAGE: 10 -->
                <!-- SHOW 5-15 -->
                <soft-pagination-item
                  v-for="index in 10"
                  :key="current_page + index - 5"
                  :label="(current_page + index + 1 - 5).toString()"
                  @click="showPage(current_page + index - 5)"
                  :active="curr_page_checker(current_page + index - 5)"
                />
                &nbsp; ... &nbsp;
                <!-- LAST PAGE -->
                <soft-pagination-item
                  :label="(query_results_chunks.length + 1 - 1).toString()"
                  @click="showPage(query_results_chunks.length - 1)"
                  :active="curr_page_checker(query_results_chunks.length - 1)"
                />
                <soft-pagination-item next @click="nextPage()" />
              </soft-pagination>
            </div>
            <!-- END - SHOW LAST PAGES -->
            <div v-else-if="current_page >= query_results_chunks.length - 6">
              <!-- <b>END</b> -->
              <soft-pagination size="sm" color="dark">
                <soft-pagination-item prev @click="prevPage()" />
                <!-- FIRST PAGE -->
                <soft-pagination-item
                  :key="'0'"
                  :label="'1'"
                  @click="showPage('0')"
                  :active="curr_page_checker('0')"
                />
                &nbsp; ... &nbsp;
                <soft-pagination-item
                  v-for="index in 12"
                  :key="(query_results_chunks.length - 13 + index).toString()"
                  :label="(query_results_chunks.length - 12 + index).toString()"
                  @click="showPage(query_results_chunks.length - 13 + index)"
                  :active="
                    curr_page_checker(query_results_chunks.length - 13 + index)
                  "
                />
                <soft-pagination-item next @click="nextPage()" />
              </soft-pagination>
            </div>
            <!-- START - SHOW FIRST FEW PAGES -->
            <div v-else>
              <!-- <b>START</b> -->
              <soft-pagination size="sm" color="dark">
                <soft-pagination-item prev @click="prevPage()" />
                <soft-pagination-item
                  v-for="index in 6"
                  :key="index - 1"
                  :label="index.toString()"
                  @click="showPage(index - 1)"
                  :active="curr_page_checker(index - 1)"
                />
                &nbsp; ... &nbsp;
                <!-- LAST PAGE -->
                <soft-pagination-item
                  :label="(query_results_chunks.length - 1 + 1).toString()"
                  @click="showPage(query_results_chunks.length - 1)"
                  :active="curr_page_checker(query_results_chunks.length - 1)"
                />
                <soft-pagination-item next @click="nextPage()" />
              </soft-pagination>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- INDIVIDUAL Article Modal -->
  <div
    class="modal fade bd-example-modal-xl"
    id="article_modal"
    tabindex="-1"
    role="dialog"
    aria-labelledby="article_modal"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-xl">
      <div v-if="isLoadingArticle" class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Loading</h5>
        </div>
        <div class="modal-body">
          <loading-topics :stage="stageOfSearch" />
        </div>
      </div>

      <div v-else class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="saveteamtitle">
            Article:
            {{
              chosen_article.headline
                ? chosen_article.headline
                : "Missing Headline"
            }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="mx-2">
            <p>
              Main Topics:
              <b
                v-for="(topic_obj, index) in article_topics"
                :key="topic_obj.topic"
                ><div v-if="index == article_topics.length - 1">
                  {{ topic_obj.topic }} <i>({{ topic_obj.score }}%)</i>
                </div>
                <div v-else>
                  {{ topic_obj.topic }} <i>({{ topic_obj.score }}%)</i>,
                </div>
              </b>
            </p>
            <!-- <p>
              Factual OR Opinionated:
              <b> {{ article_factual ? "Factual" : "Opinionated" }}</b>
            </p>v -->
            <!-- <b v-if="article_factual">Factual: ...</b>
            <b v-else>Opinionated: ...</b> -->
            <p class="form-check-label" for="flexCheckDefault">
              Date Published: <b>{{ chosen_article.date_published }}</b>
            </p>
          </div>

          <hr />
          <div class="col-sm-5"></div>
          <div class="pb-2" id="text_summariser_method">
            <div class="callout" style="font-size: smaller">
              Choose a Text Summariser Method:
            </div>
            <select
              v-model="text_summariser_method"
              class="form-control"
              name="status"
              id="status"
            >
              <option value="lc_summ">Lexical Chain</option>
              <option value="tr_summ">TextRank</option>
              <option value="tf_idf_summ">TF-IDF</option>
              <option value="ab_summ">Abstractive</option>
            </select>
          </div>
          <p>
            <b
              >Article Summary via
              <u>{{
                this.text_summariser_method == "lc_summ"
                  ? "Lexical Chain"
                  : this.text_summariser_method == "tr_summ"
                  ? "TextRank"
                  : this.text_summariser_method == "tf_idf_summ"
                  ? "TF-IDF"
                  : "Abstractive"
              }}</u
              >:</b
            >
            {{
              this.text_summariser_method == "lc_summ"
                ? this.lc_summary
                : this.text_summariser_method == "tr_summ"
                ? this.tr_summary
                : this.text_summariser_method == "tf_idf_summ"
                ? this.tf_idf_summary
                : this.ab_summary
            }}
          </p>
          <hr />

          <div class="table-responsive p-0">
            <table class="table align-items-center mb-0">
              <thead class="table align-items-center mb-0">
                <tr>
                  <th
                    class="col-3 text-wrap text-uppercase text-secondary text-xs font-weight-bolder opacity-7"
                  >
                    Entity Type
                  </th>
                  <th
                    class="col-4 text-uppercase text-secondary text-xs font-weight-bolder opacity-7"
                  >
                    Entities
                  </th>
                  <th
                    class="col-4 text-uppercase text-secondary text-xs font-weight-bolder opacity-7"
                  >
                    Count
                  </th>
                </tr>
              </thead>
              <tbody v-if="this.enitities != []">
                <tr v-for="(ent, index) in enitities" :key="index">
                  <td class="col-3 px-4 text-sm text-wrap">
                    {{ index }}
                  </td>
                  <td>
                    <tr
                      v-for="(count, nameent) in Object.fromEntries(
                        Object.entries(ent).sort((a, b) => b[1][2] - a[1][2])
                      )"
                      :key="nameent"
                      class="col-4 px-4 text-sm text-wrap"
                    >
                      <td
                        v-if="count[0] === 'Negative'"
                        class="col-3 px-4 text-sm text-wrap"
                        style="color: red"
                      >
                        {{ nameent }}
                      </td>
                      <td
                        v-if="count[0] === 'Positive'"
                        class="col-3 px-4 text-sm text-wrap"
                        style="color: green"
                      >
                        {{ nameent }}
                      </td>
                      <td
                        v-if="count[0] === 'Neutral'"
                        class="col-3 px-4 text-sm text-wrap"
                      >
                        {{ nameent }}
                      </td>
                    </tr>
                  </td>
                  <td class="col-3 px-4 text-sm text-wrap">
                    <tr
                      v-for="(count, nameent) in Object.fromEntries(
                        Object.entries(ent).sort((a, b) => b[1][2] - a[1][2])
                      )"
                      :key="nameent"
                      class="col-4 px-4 text-sm text-wrap"
                    >
                      <td class="col-3 px-4 text-sm text-wrap">
                        {{ count[2] }}
                      </td>
                    </tr>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- End Article Modal -->
</template>

<script>
import SoftPagination from "@/components/SoftPagination.vue";
import SoftPaginationItem from "@/components/SoftPaginationItem.vue";
import LoadingTopics from "./loadingSequence/LoadingTopics";

import { create, all } from "mathjs";

const config = {};
const math = create(all, config);

export default {
  components: {
    SoftPagination,
    SoftPaginationItem,

    LoadingTopics,
  },
  data() {
    return {
      companies: [
        "All Sources",
        "Atlantic",
        "BBC",
        "CNN",
        "DailyMail",
        "FOX",
        "Guardian",
        "Independent",
        "NYTimes",
        "SkyAU",
        "Washington Post",
      ],
      selected_source: "",
      chosen_article: {},
      article_factual: "",

      query_results: [],
      query_chunks: [],
      query_results_chunks: [],
      current_page_results: [],
      results_per_page: 20,
      total_results: 0,
      num_page: 0,
      isLoading: false,
      isLoadingArticle: false,
      searched: false,

      start_index: 0,
      end_index: 0,

      triggered: false,

      query_results_backup: [],
      stageOfSearch: "search",

      index: 0,
      current_page: 0,

      selected_sentiment_filter: "",
      enitities: [],
      keyword_to_search: "",
      lc_summary: "",
      chains: "",
      tf_idf_summary: "",
      tr_summary: "",
      ab_summary: "",
      text_summariser_method: "lc_summ",
      article_topics: "No Topic Found",
    };
  },

  name: "Searchbar",
  methods: {
    resetChosenTextSummariser() {
      this.text_summariser_method = "lc_summ";
    },

    // ANALYTIC FUNCTIONS GETS CALLED BY show_article() func
    // WILL RUN ALL ANALYTIC TASKS AS SOON AS WE CLICK View Article Details button --> which triggers show_article(article_obj) func
    async show_article(article) {
      this.resetChosenTextSummariser();
      this.isLoadingArticle = true;
      console.log("ARTICLE INCLUDES: ", article);
      this.stageOfSearch = "analysing_article";
      setTimeout(2000);
      // NER
      try {
        this.stageOfSearch = "analysing_article_senti";
        await fetch("http://localhost:5001/sentiment", {
          method: "post",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(article),
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
          })
          .then((data) => {
            console.log(data);
            data.data["enitity"];
            this.enitities = data.data["entity_sentiment"];
            console.log(this.enitities);
          });
      } catch (error) {
        console.log(error);
      }
      // SUMMARISATION
      try {
        this.stageOfSearch = "analysing_article_summ";
        await fetch("http://localhost:5001/summarisation", {
          method: "post",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(article),
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
          })
          .then((data) => {
            // console.log(data);
            data.data["lc_summary"];
            this.lc_summary = data.data["lc_summary"];
            data.data["chains"];
            this.chains = data.data["chains"];
            data.data["tf_idf_summary"];
            this.tf_idf_summary = data.data["tf_idf_summary"];
            // console.log(data.data["tr_summary"]);
            this.tr_summary = data.data["tr_summary"];
            console.log(data.data["ab_summary"][0]);
            this.ab_summary = data.data["ab_summary"][0];
            // console.log(this.lc_summary);
            // console.log(this.chains);
            // console.log(this.tf_idf_summary);
            // console.log(this.tr_summary);
          });
      } catch (error) {
        console.log(error);
      }
      // TOPIC MODELLING
      try {
        this.stageOfSearch = "analysing_article_topic";
        await fetch("http://localhost:5001/ldatopic", {
          method: "post",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(article),
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
          })
          .then((data) => {
            // console.log("TOPICS MODELLING: ", data);
            data.data["dominant_topic"];
            var topic_overall = data.data["topics_overall"];
            // console.log("BEFORE: ", topic_overall);
            // SORT TOPICS BY SCORE
            topic_overall.sort((a, b) => b.score - a.score); // b - a for reverse sort
            this.article_topics = topic_overall;

            // console.log("AFTER: ", topic_overall);
          });
      } catch (error) {
        console.log(error);
      }

      this.chosen_article = article;
      // The best: lc_summ, 2nd: tr_summ, 3rd: tf_idf_summ, last: ab_summ
      // console.log(this.entities);
      // console.log(this.lc_summary);
      // console.log(this.chains);
      // console.log(this.tf_idf_summary);
      // console.log(this.tr_summary);
      this.isLoadingArticle = false;
      this.stageOfSearch = "search";
    },

    showPage(index) {
      this.current_page_results = this.query_results_chunks[index];
      this.current_page = index;
      setTimeout(() => {
        // console.log("CURRENT PAGE: ", this.query_results_chunks[index]);
      }, 2000);
    },

    nextPage() {
      if (this.current_page < this.query_results_chunks.length - 1) {
        this.current_page += 1;
      } else {
        console.log("No more pages to load");
      }
    },

    prevPage() {
      if (this.current_page != 0) {
        this.current_page -= 1;
      } else {
        console.log("No more pages to load");
      }
    },

    clearData() {
      this.query_results = [];
      this.searched = false;
      this.query_results_chunks = [];
      this.total_results = 0;
      this.query_chunks = [];
      this.start_index = 0;
      this.end_index = 0;
      this.num_page = 0;

      this.query_results_backup = [];
      this.stageOfSearch = "search";

      this.selected_sentiment_filter = "all";
      this.keyword_to_search = "";
    },

    resetSearch() {
      // To run everytime user clicks Search again
      this.query_results = [];
      this.searched = false;
      this.query_results_chunks = [];
      this.total_results = 0;
      this.query_chunks = [];
      this.start_index = 0;
      this.end_index = 0;
      this.num_page = 0;
      // Search Tabs

      this.query_results_backup = [];

      this.selected_sentiment_filter = "all";
    },

    async get_articles() {
      // CHECK IF USER HAS ALREADY SEARCHED
      // MEANING THE query_results should be filled
      this.current_page = 0;
      this.searched = true;
      // console.log(
      //   "INSIDE get_articles",
      //   this.selected_source,
      //   this.keyword_to_search
      // );
      if (this.selected_source != "") {
        try {
          this.isLoading = true;
          await fetch(
            "http://localhost:5001/get_articles/" + this.selected_source
          )
            .then((response) => {
              if (response.ok) {
                // console.log(response);
                return response.json();
              }
            })
            .then((data) => {
              // console.log("!!!Data found!!!");
              // NEXT CHECK IF USER HAS TYPED ANYTHING UNDER SEARCH BY KEYWORDS... keyword_to_search
              if ("data" in data) {
                if ("articles" in data.data) {
                  if (this.keyword_to_search != "") {
                    // Loop thru this.query_results and only show articles with "keyword_to_search" in headline...
                    let keyword = this.keyword_to_search.toLowerCase();
                    var new_list_of_results = [];

                    // CHECK IF KEYWORD IS A SINGLE WORD OR PHRASE
                    // IF SINGLE WORD: do split and search if in list
                    if (!keyword.includes(" ")) {
                      for (const article_obj of data.data.articles) {
                        const temp_headline_lower_arr = article_obj.headline.toLowerCase();
                        var punctuationless = temp_headline_lower_arr.replace(
                          /[.,/#!$%^&*;:{}=\-_`~():]/g,
                          ""
                        );
                        var finalStringArr = punctuationless
                          .replace(/\s{2,}/g, " ")
                          .split(" ");
                        for (const str of finalStringArr) {
                          if (str.includes(keyword)) {
                            new_list_of_results.push(article_obj);
                            break;
                          }
                        }
                      }
                    } else {
                      //  ELSE IF PHRASE: just do .includes(keyword)
                      for (const article_obj of data.data.articles) {
                        const temp_headline_lower_arr = article_obj.headline.toLowerCase();

                        if (temp_headline_lower_arr.includes(keyword)) {
                          new_list_of_results.push(article_obj);
                        }
                      }
                    }

                    this.query_results = new_list_of_results;
                  } else {
                    this.query_results = data.data.articles;
                  }

                  this.query_results_backup = data.data.articles;
                }
              }
            });
        } catch (error) {
          console.error;
          console.log("!!!No News Articles found!!!");
          await this.setPagination();
          this.isLoading = false;
        }
      }

      this.current_page_results = this.query_results.slice(0, 20);

      await this.setPagination();
      this.isLoading = false;
    },

    curr_page_checker(page_num) {
      if (page_num == this.current_page) {
        return true;
      } else {
        return false;
      }
    },
    async setPagination() {
      this.query_results_chunks = [];
      this.query_chunks = [];
      this.num_page = math.ceil(
        this.query_results.length / this.results_per_page
      );
      // console.log("In Pagination", this.query_results);
      for (let i = 0; i < this.num_page; i++) {
        // some code
        if (this.num_page <= 1) {
          this.start_index = 0;
          this.end_index = this.query_results.length;
        } else {
          this.start_index = i * this.results_per_page;
          this.end_index = (i + 1) * this.results_per_page - 1;
        }
        this.query_chunks = this.query_results.slice(
          this.start_index,
          this.end_index + 1
        );
        this.query_results_chunks.push(this.query_chunks);
      }
      this.showPage(0);
    },

    async filterMaster(event) {
      var list_of_results = this.query_results_backup;

      const intent = event.target.value;
      if (intent.includes("date")) {
        // sort by date published: either Most Recent OR Least Recent
        if (intent == "dateMostRecent") {
          // console.log("Sorting by MOST Recent");
          list_of_results = this.sortByDatePublished(list_of_results, true);
        } else {
          // console.log("Sorting by LEAST Recent");
          list_of_results = this.sortByDatePublished(list_of_results, false);
        }
      } else if (intent.includes("article")) {
        // sort by article length: either Longest or Shortest
        if (intent == "articleLengthLongest") {
          // console.log("Sorting by Longest article");
          list_of_results = this.sortByArticleLength(list_of_results, true);
        } else {
          // console.log("Sorting by Shortest article");
          list_of_results = this.sortByArticleLength(list_of_results, false);
        }
      }
      // 2021-12-08 11:00:00

      this.query_results = list_of_results;
      this.showPage(0);
      await this.setPagination();
      return;
    },

    sortByDatePublished(list_of_results, MostRecent) {
      // console.log("STEP 1");
      var new_list_of_results = [];
      if (list_of_results.length > 0) {
        new_list_of_results = list_of_results;
      }

      // console.log("STEP 2");
      if (MostRecent == true) {
        new_list_of_results.sort(
          (a, b) =>
            this.convert_date_to_numeric(b.date_published) -
            this.convert_date_to_numeric(a.date_published)
        );
      } else {
        new_list_of_results.sort(
          (a, b) =>
            this.convert_date_to_numeric(a.date_published) -
            this.convert_date_to_numeric(b.date_published)
        );
      }
      return new_list_of_results;
    },

    sortByArticleLength(list_of_results, byLongest) {
      // console.log("STEP 1");
      var new_list_of_results = [];
      if (list_of_results.length > 0) {
        new_list_of_results = list_of_results;

        // console.log("STEP 2");
        if (byLongest == true) {
          new_list_of_results.sort(
            (a, b) => b.article_length - a.article_length
          );
        } else {
          new_list_of_results.sort(
            (a, b) => a.article_length - b.article_length
          );
        }
        return new_list_of_results;
      } else {
        // JUST RETURN THE ORIGINAL LIST BACK
        return this.query_results_backup;
      }
    },

    sort_sentiment_score(a, b) {
      if (a.sentiment_score < b.sentiment_score) {
        return -1;
      }
      if (a.sentiment_score > b.sentiment_score) {
        return 1;
      }
      return 0;
    },

    // HELPERFUNC FOR SORTING BY DATE (MOST RECENT or LEAST RECENT)
    convert_date_to_numeric(date_str) {
      // console.log("STEP 3");
      if (date_str != "-" || date_str != "") {
        let temp_arr = [];
        if (date_str.includes("-")) {
          // 2021-12-08 16:03:00
          // to 20211208160300
          const temp_date_details_arr = date_str.split(" ");
          const date_pub = temp_date_details_arr[0].split("-");
          const time_pub = temp_date_details_arr[1].split(":");
          temp_arr = [date_pub.join(""), time_pub.join("")];
        } else if (date_str.includes("/")) {
          // 27/8/2019 16:03
          // to 20190827160300
          const temp_date_details_arr = date_str.split(" ");
          const date_pub = temp_date_details_arr[0].split("/");
          let time_pub = temp_date_details_arr[1].split(":");
          // time: 01:00
          if (time_pub[0].length == 1) {
            time_pub[0] = "0" + time_pub[0];
          }
          time_pub.push("00");

          const year = date_pub[2];
          let month = date_pub[1];
          let day = date_pub[0];

          // 1 --> 01
          if (month.length == 1) {
            month = "0" + month;
          }
          // 1 --> 01
          if (day.length == 1) {
            day = "0" + day;
          }
          const date_numerical = year + month + day;

          temp_arr = [date_numerical, time_pub.join("")];
        }
        // console.log(temp_arr.join("").length);
        return temp_arr.join("");
      } else {
        return 0;
      }
    },
  },

  // Methods END

  //   created() {
  //     this.getCompanies();
  //     // Retreive user's previously saved search queries
  //     this.retrievePersonal();
  //   },
};
</script>
