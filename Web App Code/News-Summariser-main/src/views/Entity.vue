<template>
  <div class="py-2 container-fluid">
    <div class="row px-1">
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
              <div class="col-lg-10 d-flex flex-column">
                <!-- <div><canvas id="bubble"></canvas></div><br/> -->
                <div>Joint Sentiment Entity Charts</div>
                <div id="bubblePERSON"></div>
                <div id="bubbleORG"></div>
                <div id="bubbleCLIMATE"></div>
                <div id="bubbleGPE"></div>
                <div id="bubbleLOC"></div>
                <div id="bubbleEVENT"></div>

                <div class="mt-3 mb-3">Entity Frequency Charts</div>
                <div style="margin-left: 100px">
                  <div style="width: 750px"><canvas id="org"></canvas></div>
                  <div style="width: 750px"><canvas id="per"></canvas></div>
                  <div style="width: 750px"><canvas id="climate"></canvas></div>
                  <div style="width: 750px"><canvas id="event"></canvas></div>
                </div>

                <div class="mt-3 mb-3">LDA Charts</div>
                <div class="col-lg-10 d-flex flex-column">
                  <h6 class="my-2">Select Topic</h6>
                  <div class="row">
                    <div class="row my-2">
    
                      <form role="form" id="company-form" autocomplete="off">
                        <v-select
                          :options="topics"
                          style="font-size: smaller; --vs-border-radius: 6px"
                          v-model="selected_topic"
                        >
                        </v-select>
                      </form>
                    </div>
                    <div>
                      <span>
                        <button
                          type="submit"
                          class="btn bg-gradient-custom"
                          @click="create_lda(this.selected_topic)"
                        >
                          Get
                        </button>
                      </span>
                    </div>
                  </div>
                </div>
                <div style="margin-left: 100px">
                  <div v-if="this.load" class="mt-3 mb-3">{{ this.selected_topic }}</div>
                  <div style="width: 750px">
                    <canvas id="ldaclimate"></canvas>
                  </div>
                  <div style="width: 750px"><canvas id="ldaorg"></canvas></div>
                  <div style="width: 750px"><canvas id="ldaper"></canvas></div>
                  <div style="width: 750px">
                    <canvas id="ldaevent"></canvas>
                  </div>
                  <div style="width: 750px"><canvas id="ldagpe"></canvas></div>
                  <div style="width: 750px"><canvas id="ldaloc"></canvas></div>
                </div>

                
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- End Article Modal -->
</template>

<script>
import { FLOWBASEANNOTATION_TYPES } from "@babel/types";
import Chart from "chart.js/auto";
import * as echarts from "echarts";
export default {
  components: {},
  data() {
    return {
      load:false,
      selected_topic: "",
      orglabel: [],
      org: [],
      perlabel: [],
      per: [],
      climatelabel: [],
      climate: [],
      eventlabel: [],
      event: [],
      PERSONbubble: [],
      ORGbubble: [],
      CLIMATEbubble: [],
      GPEbubble: [],
      LOCbubble: [],
      EVENTbubble: [],
      lda: [],
      cchart:"",
      ochart:"",
      pchart:"",
      echart:"",
      lchart:"",
      gchart:"",
      topics:["Environmental Impact","Social Impact","Environmental Politics","Economic Impact"]
    };
  },

  name: "Entity",
  methods: {
    async show_org() {
      try {
        await fetch("http://localhost:5002/orgbar")
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
          })
          .then((data) => {
            console.log(data);
            this.orglabel = data.data.entity;
            this.org = data.data.values;
          });
      } catch (error) {
        console.log(error);
      }
      new Chart(document.getElementById("org"), {
        type: "bar",
        data: {
          labels: this.orglabel,
          datasets: [
            {
              label: "Organisation",
              data: this.org,
              backgroundColor: "#9BD0F5",
            },
          ],
        },
      });
    },
    async show_per() {
      try {
        await fetch("http://localhost:5002/perbar")
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
          })
          .then((data) => {
            console.log(data);
            this.perlabel = data.data.entity;
            this.per = data.data.values;
          });
      } catch (error) {
        console.log(error);
      }
      new Chart(document.getElementById("per"), {
        type: "bar",
        data: {
          labels: this.perlabel,
          datasets: [
            {
              label: "Person",
              data: this.per,
              backgroundColor: "#ac6abd",
            },
          ],
        },
      });
    },
    async show_climate() {
      try {
        await fetch("http://localhost:5002/climatebar")
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
          })
          .then((data) => {
            console.log(data);
            this.climatelabel = data.data.entity;
            this.climate = data.data.values;
          });
      } catch (error) {
        console.log(error);
      }
      new Chart(document.getElementById("climate"), {
        type: "bar",
        data: {
          labels: this.climatelabel,
          datasets: [
            {
              label: "Climate",
              data: this.climate,
              backgroundColor: "#00b300",
            },
          ],
        },
      });
    },
    async show_event() {
      try {
        await fetch("http://localhost:5002/eventbar")
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
          })
          .then((data) => {
            console.log(data);
            this.eventlabel = data.data.entity;
            this.event = data.data.values;
          });
      } catch (error) {
        console.log(error);
      }
      new Chart(document.getElementById("event"), {
        type: "bar",
        data: {
          labels: this.eventlabel,
          datasets: [
            {
              label: "Event",
              data: this.event,
              backgroundColor: "#dbd15e",
            },
          ],
        },
      });
    },
    async show_bubble() {
      try {
        await fetch("http://localhost:5002/sentiment")
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
          })
          .then((data) => {
            console.log(data);

            for (var pname in data.data.person) {
              var ppoint = [
                data.data.person[pname][0],
                data.data.person[pname][1],
                pname,
              ];
              this.PERSONbubble.push(ppoint);
            }
            for (var oname in data.data.org) {
              var opoint = [
                data.data.org[oname][0],
                data.data.org[oname][1],
                oname,
              ];
              this.ORGbubble.push(opoint);
            }
            for (var lname in data.data.loc) {
              var lpoint = [
                data.data.loc[lname][0],
                data.data.loc[lname][1],
                lname,
              ];
              this.LOCbubble.push(lpoint);
            }
            for (var gname in data.data.gpe) {
              var gpoint = [
                data.data.gpe[gname][0],
                data.data.gpe[gname][1],
                gname,
              ];
              this.GPEbubble.push(gpoint);
            }
            for (var ename in data.data.event) {
              var epoint = [
                data.data.event[ename][0],
                data.data.event[ename][1],
                ename,
              ];
              this.EVENTbubble.push(epoint);
            }
            for (var cname in data.data.climate) {
              var cpoint = [
                data.data.climate[cname][0],
                data.data.climate[cname][1],
                cname,
              ];
              this.CLIMATEbubble.push(cpoint);
            }
          });
      } catch (error) {
        console.log(error);
      }

      this.createchart("PERSON", this.PERSONbubble);
      this.createchart("ORG", this.ORGbubble);
      this.createchart("LOC", this.LOCbubble);
      this.createchart("GPE", this.GPEbubble);
      this.createchart("EVENT", this.EVENTbubble);
      this.createchart("CLIMATE", this.CLIMATEbubble);
    },
    createchart(ent, data) {
      var chartDom = document.getElementById("bubble" + ent);
      var Chart = echarts.init(chartDom);
      var option;
      Chart.resize({ height: 500, width: 1000 });
      window.addEventListener("resize", { passive: true }, function () {
        Chart.resize({ height: 500, width: 1000 });
      });

      option = {
        xAxis: {
          name: "Sentiment",
        },
        yAxis: {
          scale: true,
          name: ent,
        },
        series: [
          {
            name: ent,
            data: data,
            type: "scatter",
            symbolSize: function (data) {
              return Math.sqrt(data[1]);
            },
            emphasis: {
              focus: "series",
              label: {
                show: true,
                position: "top",
              },
            },
            label: {
              show: false,
              formatter: function (param) {
                return param.data[2];
              },
              minMargin: 10,
              position: "top",
            },
          },
        ],
        visualMap: {
          orient: "horizontal",
          left: "center",
          min: -0.1,
          max: 0.1,

          // Map the score column to color
          dimension: 0,
          inRange: {
            color: ["#fc0303", "#03fc8c"],
          },
          text: ["1", "-1"],
        },
        tooltip: {
          backgroundColor: "rgba(255,255,255,0.7)",
          formatter: function (param) {
            var value = param.value;
            // prettier-ignore
            return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">'
                          + value[2]
                          + '</div>'
                          + "Sentiment" + '：' + value[0] + '<br>'
                          + "Count" + '：' + value[1] + '<br>'
                          ;
          },
        },
      };

      option && Chart.setOption(option);
    },
    async ldachart() {
      try {
        await fetch("http://localhost:5002/lda")
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
          })
          .then((data) => {
            // console.log(data);
            this.lda = data.data.lda;
            console.log(this.lda);
            // this.topic1 = data.data.lda[0];
            // this.topic2 = data.data.lda[1];
            // this.topic3 = data.data.lda[2];
            // this.topic4 = data.data.lda[3];
            // console.log(this.topic1);
            // this.create_lda("Environmental Impact", this.topic1);
          });
      } catch (error) {
        console.log(error);
      }
    },
    create_lda(topic) {
      console.log(topic)
      var data=[]
      if(this.cchart){
        this.cchart.destroy();
      }
      if(this.gchart){
        this.gchart.destroy();
      }
      if(this.pchart){
        this.pchart.destroy();
      }
      if(this.lchart){
        this.lchart.destroy();
      }
      if(this.echart){
        this.echart.destroy();
      }
      if(this.ochart){
        this.ochart.destroy();
      }
      if(topic=="Environmental Impact"){
        console.log('yes')
        data=this.lda[0]
        console.log(data)
      }
      else if(topic=="Social Impact"){
        data=this.lda[1]
      }
      else if(topic=="Environmental Politics"){
        data=this.lda[2]
      }
      else if(topic=="Economic Impact"){
        data=this.lda[3]
      }
      var climatedata = data.climate;
      var climatelabel = [];
      var climatept = [];
      // console.log(climatedata)
      for (var p in climatedata) {
        // console.log(p)
        climatelabel.push(climatedata[p][0]);
        climatept.push(climatedata[p][1]);
      }
      // console.log(climatelabel)
      var orgdata = data.org;
      var orglabel = [];
      var orgpt = [];
      for (var op in orgdata) {
        orglabel.push(orgdata[op][0]);
        orgpt.push(orgdata[op][1]);
      }

      var perdata = data.person;
      var perlabel = [];
      var perpt = [];
      for (var pp in perdata) {
        perlabel.push(perdata[pp][0]);
        perpt.push(perdata[pp][1]);
      }

      var eventdata = data.event;
      var eventlabel = [];
      var eventpt = [];
      for (var ep in eventdata) {
        eventlabel.push(eventdata[ep][0]);
        eventpt.push(eventdata[ep][1]);
      }

      var locdata = data.loc;
      var loclabel = [];
      var locpt = [];
      for (var lp in locdata) {
        loclabel.push(locdata[lp][0]);
        locpt.push(locdata[lp][1]);
      }

      var gpedata = data.gpe;
      var gpelabel = [];
      var gpept = [];
      for (var gp in gpedata) {
        gpelabel.push(gpedata[gp][0]);
        gpept.push(gpedata[gp][1]);
      }

      this.cchart=new Chart(document.getElementById("ldaclimate"), {
        type: "bar",
        data: {
          labels: climatelabel,
          datasets: [
            {
              label: "Climate",
              data: climatept,
              backgroundColor: "#00b300",
            },
          ],
        },
      });
      this.gchart=new Chart(document.getElementById("ldagpe"), {
        type: "bar",
        data: {
          labels: gpelabel,
          datasets: [
            {
              label: "GPE",
              data: gpept,
              backgroundColor: "#a97ecc",
            },
          ],
        },
      });
      this.lchart=new Chart(document.getElementById("ldaloc"), {
        type: "bar",
        data: {
          labels: loclabel,
          datasets: [
            {
              label: "Location",
              data: locpt,
              backgroundColor: "#3291a8",
            },
          ],
        },
      });
      this.echart=new Chart(document.getElementById("ldaevent"), {
        type: "bar",
        data: {
          labels: eventlabel,
          datasets: [
            {
              label: "Event",
              data: eventpt,
              backgroundColor: "#a8a432",
            },
          ],
        },
      });
      this.pchart=new Chart(document.getElementById("ldaper"), {
        type: "bar",
        data: {
          labels: perlabel,
          datasets: [
            {
              label: "Person",
              data: perpt,
              backgroundColor: "#32a887",
            },
          ],
        },
      });
      this.ochart=new Chart(document.getElementById("ldaorg"), {
        type: "bar",
        data: {
          labels: orglabel,
          datasets: [
            {
              label: "Organisation",
              data: orgpt,
              backgroundColor: "#cc7eae",
            },
          ],
        },
      });
      this.load=true
    },
    
  },

  // Methods END

  created() {
    this.show_org();
    this.show_per();
    this.show_climate();
    this.show_event();
    this.show_bubble();
    this.ldachart();
  },
};
</script>
