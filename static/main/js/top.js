let minSize = {min: 140, max: 250}
let mediumSize = {min: 250, max: 400}
let largeSize = {min: 400, max: 600}

const app1 = new Vue({
    el: "#top",
    delimiters: ['[[', ']]'],
    data: {
        min: 0,
        max: 0,
        searchWord: "",
        isSearch: false,
        isSmall: false,
        isMedium: false,
        isLarge: false,
        isMug: false,
        isGlass: false,
        isStainless: false,
        searchUrl: "",
    },
    computed: {
        watchObject() {
            return [this.isSearch, this.isSmall, this.isMedium, this.isLarge, this.isMug, this.isGlass, this.isStainless]
        },
    },
    watch: {
        watchObject(val) {
            if (!(this.isSearch)) {
                console.log("exit")
                exit;
            }
            if (this.isSmall) {
                this.min = minSize["min"];
                this.max = minSize["max"];
            }
            if (this.isMedium) {
                this.min = mediumSize["min"];
                this.max = mediumSize["max"];
            }
            if (this.isLarge) {
                this.min = largeSize["min"];
                this.max = largeSize["max"];
            }
            if (this.isMug) {
                this.searchWord = "マグカップ"
            }
            if (this.isGlass) {
                this.searchWord = "グラス"
            }
            if (this.isStainless) {
                this.searchWord = "ステンレス"
            }
            if (this.searchWord == "") {
                this.searchUrl = `/cup/list?min_capacity=${this.min}&max_capacity=${this.max}`
            } else {
                this.searchUrl = `/cup/list?min_capacity=${this.min}&max_capacity=${this.max}&search_material=${this.searchWord}`
            }
        }
    },
    methods: {
        createUrl: function () {
            if (!(this.isSearch)) {
                console.log("exit")
                exit;
            }
            if (this.isSmall) {
                this.min = minSize["min"];
                this.max = minSize["max"];
            }
            if (this.isMedium) {
                this.min = mediumSize["min"];
                this.max = mediumSize["max"];
            }
            if (this.isLarge) {
                this.min = largeSize["min"];
                this.max = largeSize["max"];
            }
            if (this.isMug) {
                this.searchWord = "マグカップ"
            }
            if (this.isGlass) {
                this.searchWord = "グラス"
            }
            if (this.isStainless) {
                this.searchWord = "ステンレス"
            }
            if (this.searchWord == "") {
                this.searchUrl = `/cup/list?min_capacity=${this.min}&max_capacity=${this.max}`
            } else {
                this.searchUrl = `/cup/list?min_capacity=${this.min}&max_capacity=${this.max}&search_material=${this.searchWord}`
            }
        },
        changeSizeBool: function (size) {

            if (size == "small") {
                this.isSmall = true;
                this.isMedium = false;
                this.isLarge = false;
                this.isSearch = true;
            } else if (size == "medium") {
                this.isSmall = false;
                this.isMedium = true;
                this.isLarge = false;
                this.isSearch = true;
            } else if (size == "large") {
                this.isSmall = false;
                this.isMedium = false;
                this.isLarge = true;
                this.isSearch = true;
            }
        },
        changeMaterialBool: function (material) {

            if (material == "mug") {
                this.isMug = true;
                this.isGlass = false;
                this.isStainless = false;

            } else if (material == "glass") {
                this.isMug = false;
                this.isGlass = true;
                this.isStainless = false;

            } else if (material == "stainless") {
                this.isMug = false;
                this.isGlass = false;
                this.isStainless = true;
            }

        },
    },

})

const swiper = new Swiper('.swiper', {
    // Optional parameters
    // direction: 'vertical',
    loop: true,
    grabCursor:true,
    effect: "coverflow",
    centeredSlides: true,
    slidesPerView: 1,
    speed: 1000,
    autoplay: {
        delay: 4000,
        disableOnInteraction: false,
    }
});