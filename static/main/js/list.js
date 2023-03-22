Vue.component("modal", {
    template: "#modal-template",
    delimiters: ['[[', ']]'],
    data() {
        return {
            selectsPrice: [
                {id: 1, label: "0 ～ 1,500円", min_price: 0, max_price: 1500},
                {id: 2, label: "1,500 ～ 5,000円", min_price: 1500, max_price: 5000},
                {id: 3, label: "5,000 ～ 10,000円", min_price: 5000, max_price: 10000},
                {id: 4, label: "10,000 ～ 30,000円", min_price: 10000, max_price: 30000},
                {id: 5, label: "30,000円 ～ ", max_price: 300000},
            ],
            selectedPrice: 0,
            selectsCapacity: [
                {id: 1, label: "150 ～ 250ml", min_capacity: 150, max_capacity: 250},
                {id: 2, label: "250 ～ 400ml", min_capacity: 250, max_capacity: 400},
                {id: 3, label: "400 ～ 600ml", min_capacity: 400, max_capacity: 600},
            ],
            selectedCapacity: 0,
            selectsMaterial: [
                {id: 1, label: "マグカップ"},
                {id: 2, label: "グラス"},
                {id: 3, label: "ステンレス"},
            ],
            selectedMaterial: 0,
            selectsSort: [
                {id: 1, label: "容量順", sort: "capacity"},
                {id: 2, label: "値段順", sort: "price"},
            ],
            selectedSort: 0,
            queryParams: {},
            queryUrl: "",
        }
    },
    computed: {
        watchObject() {
            return [this.selectedPrice, this.selectedCapacity, this.selectedMaterial, this.selectedSort]
        },
    },
    watch: {
        selectedPrice: function () {
            delete this.queryParams["min_price"]
            delete this.queryParams["max_price"]
            if (!(this.selectsPrice[this.selectedPrice - 1]["min_price"] === undefined)) {
                this.queryParams["min_price"] = this.selectsPrice[this.selectedPrice - 1]["min_price"];
            }
            this.queryParams["max_price"] = this.selectsPrice[this.selectedPrice - 1]["max_price"];
            console.log(this.queryParams)
        },
        selectedCapacity: function () {
            delete this.queryParams["min_capacity"]
            delete this.queryParams["max_capacity"]
            this.queryParams["min_capacity"] = this.selectsCapacity[this.selectedCapacity - 1]["min_capacity"];
            this.queryParams["max_capacity"] = this.selectsCapacity[this.selectedCapacity - 1]["max_capacity"];
            console.log(this.queryParams)
        },
        selectedMaterial: function () {
            delete this.queryParams["search_material"]
            this.queryParams["search_material"] = this.selectsMaterial[this.selectedMaterial - 1]["label"];
            console.log(this.queryParams)
        },
        selectedSort: function () {
            delete this.queryParams["sort"]
            this.queryParams["sort"] = this.selectsSort[this.selectedSort - 1]["sort"];
            console.log(this.queryParams)
        },
        watchObject(val) {
            const urlSearchParam = new URLSearchParams(this.queryParams).toString();
            this.queryUrl = "?" + urlSearchParam
            console.log(this.queryUrl)
        },
    }
});

// start app
const app = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data() {
        return {
            showModal: false,
        };
    },
});
