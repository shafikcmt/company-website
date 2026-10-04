/*
 * Humana Apparels — public site behaviour. Vanilla JS, no dependencies.
 *
 *   [data-site-header]          sticky header that condenses on scroll
 *   [data-drawer]               mobile navigation drawer
 *   [data-reveal]               scroll reveal: up | left | right | fade
 *                               (+ data-reveal-delay="120" in ms)
 *   [data-count-to]             count-up number (data-prefix / data-suffix)
 *   [data-hero]                 home hero carousel
 *   [data-tabs]                 accessible tabs (role=tab / role=tabpanel)
 *   [data-filter]               filter buttons for [data-filter-item] grids
 *   [data-lightbox]             image lightbox (grouped by data-lightbox)
 *   [data-back-to-top]          back-to-top button
 */
(function () {
    "use strict";

    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    function $all(selector, root) {
        return Array.prototype.slice.call((root || document).querySelectorAll(selector));
    }

    function onReady(fn) {
        if (document.readyState !== "loading") fn();
        else document.addEventListener("DOMContentLoaded", fn);
    }

    /* ------------------------------------------------------------ */
    /* Header                                                       */
    /* ------------------------------------------------------------ */
    function initHeader() {
        var header = document.querySelector("[data-site-header]");
        if (!header) return;
        var ticking = false;
        function update() {
            header.classList.toggle("is-scrolled", window.scrollY > 12);
            ticking = false;
        }
        window.addEventListener(
            "scroll",
            function () {
                if (!ticking) {
                    window.requestAnimationFrame(update);
                    ticking = true;
                }
            },
            { passive: true }
        );
        update();
    }

    /* ------------------------------------------------------------ */
    /* Mobile drawer                                                */
    /* ------------------------------------------------------------ */
    function initDrawer() {
        var drawer = document.querySelector("[data-drawer]");
        var backdrop = document.querySelector("[data-drawer-backdrop]");
        var toggles = $all("[data-drawer-toggle]");
        if (!drawer || !toggles.length) return;
        var lastFocus = null;

        function focusables() {
            return $all("a[href], button:not([disabled])", drawer);
        }

        function setOpen(open) {
            drawer.classList.toggle("is-open", open);
            if (backdrop) backdrop.classList.toggle("is-open", open);
            drawer.setAttribute("aria-hidden", open ? "false" : "true");
            if (open) drawer.removeAttribute("inert");
            else drawer.setAttribute("inert", "");
            toggles.forEach(function (t) {
                t.setAttribute("aria-expanded", open ? "true" : "false");
            });
            document.documentElement.style.overflow = open ? "hidden" : "";
            if (open) {
                lastFocus = document.activeElement;
                var first = focusables()[0];
                if (first) window.setTimeout(function () { first.focus(); }, 50);
            } else if (lastFocus) {
                lastFocus.focus();
            }
        }

        toggles.forEach(function (t) {
            t.addEventListener("click", function () {
                setOpen(!drawer.classList.contains("is-open"));
            });
        });
        $all("[data-drawer-close]").forEach(function (b) {
            b.addEventListener("click", function () { setOpen(false); });
        });
        if (backdrop) backdrop.addEventListener("click", function () { setOpen(false); });

        document.addEventListener("keydown", function (e) {
            if (!drawer.classList.contains("is-open")) return;
            if (e.key === "Escape") {
                setOpen(false);
            } else if (e.key === "Tab") {
                // Keep keyboard focus inside the open drawer.
                var items = focusables();
                if (!items.length) return;
                var first = items[0], last = items[items.length - 1];
                if (e.shiftKey && document.activeElement === first) {
                    e.preventDefault();
                    last.focus();
                } else if (!e.shiftKey && document.activeElement === last) {
                    e.preventDefault();
                    first.focus();
                }
            }
        });

        // Close when switching to the desktop layout.
        window.matchMedia("(min-width: 1280px)").addEventListener("change", function (mq) {
            if (mq.matches) setOpen(false);
        });
    }

    /* ------------------------------------------------------------ */
    /* Scroll reveal                                                */
    /* ------------------------------------------------------------ */
    function initReveal() {
        var els = $all("[data-reveal]");
        if (!els.length) return;
        els.forEach(function (el) {
            var delay = parseInt(el.getAttribute("data-reveal-delay") || "0", 10);
            if (delay) el.style.transitionDelay = delay + "ms";
        });
        if (!("IntersectionObserver" in window)) {
            els.forEach(function (el) { el.classList.add("is-revealed"); });
            return;
        }
        var io = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-revealed");
                        io.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
        );
        els.forEach(function (el) { io.observe(el); });
    }

    /* ------------------------------------------------------------ */
    /* Count-up                                                     */
    /* ------------------------------------------------------------ */
    function formatNumber(n) {
        return Math.round(n).toLocaleString("en-US");
    }

    function initCountUp() {
        var els = $all("[data-count-to]");
        if (!els.length) return;

        function render(el, value) {
            el.textContent =
                (el.getAttribute("data-prefix") || "") +
                formatNumber(value) +
                (el.getAttribute("data-suffix") || "");
        }

        function run(el) {
            var target = parseFloat(el.getAttribute("data-count-to"));
            if (isNaN(target)) return;
            if (reduceMotion.matches) return render(el, target);
            var duration = 1500, start = null;
            function step(ts) {
                if (start === null) start = ts;
                var p = Math.min((ts - start) / duration, 1);
                var eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
                render(el, target * eased);
                if (p < 1) window.requestAnimationFrame(step);
            }
            window.requestAnimationFrame(step);
        }

        if (!("IntersectionObserver" in window) || reduceMotion.matches) {
            els.forEach(function (el) {
                render(el, parseFloat(el.getAttribute("data-count-to")) || 0);
            });
            return;
        }
        // Start from zero only once JS is known to run (server renders the final value).
        els.forEach(function (el) { render(el, 0); });
        var io = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        run(entry.target);
                        io.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.5 }
        );
        els.forEach(function (el) { io.observe(el); });
    }

    /* ------------------------------------------------------------ */
    /* Hero carousel                                                */
    /* ------------------------------------------------------------ */
    function initHero() {
        var hero = document.querySelector("[data-hero]");
        if (!hero) return;

        // Staggered text reveal on load.
        window.requestAnimationFrame(function () {
            window.requestAnimationFrame(function () { hero.classList.add("is-ready"); });
        });

        var slides = $all("[data-hero-slide]", hero);
        if (slides.length < 2) return;

        var dots = $all("[data-hero-dot]", hero);
        var current = hero.querySelector("[data-hero-current]");
        var toggle = hero.querySelector("[data-hero-toggle]");
        var media = hero.querySelector("[data-hero-media]") || hero;
        var autoplay = hero.getAttribute("data-autoplay") === "true";
        var interval = Math.max(2, parseFloat(hero.getAttribute("data-interval")) || 6) * 1000;

        var index = 0;
        var elapsed = 0;
        var lastTs = null;
        var userPaused = !autoplay || reduceMotion.matches;
        var hoverPaused = false;
        var hiddenPaused = false;

        hero.style.setProperty("--hero-interval", interval / 1000 + "s");

        function pad(n) { return n < 10 ? "0" + n : String(n); }

        function isPaused() { return userPaused || hoverPaused || hiddenPaused; }

        function syncPausedState() {
            hero.classList.toggle("is-paused", isPaused());
            if (toggle) {
                toggle.setAttribute("aria-pressed", userPaused ? "true" : "false");
                toggle.setAttribute(
                    "aria-label",
                    userPaused ? toggle.getAttribute("data-label-play") : toggle.getAttribute("data-label-pause")
                );
                $all("[data-icon-play]", toggle).forEach(function (i) { i.hidden = !userPaused; });
                $all("[data-icon-pause]", toggle).forEach(function (i) { i.hidden = userPaused; });
            }
        }

        function setProgress(p) {
            dots.forEach(function (dot, i) {
                dot.style.setProperty("--progress", i === index ? p : 0);
            });
        }

        function go(next) {
            var target = (next + slides.length) % slides.length;
            if (target === index) return;
            slides[index].classList.remove("is-active");
            slides[index].setAttribute("aria-hidden", "true");
            index = target;
            var slide = slides[index];
            // Lazy images: make sure the incoming slide is requested now.
            var img = slide.querySelector("img[loading='lazy']");
            if (img) img.loading = "eager";
            // Restart the Ken Burns animation on the incoming image.
            if (img) { img.style.animation = "none"; void img.offsetWidth; img.style.animation = ""; }
            slide.classList.add("is-active");
            slide.removeAttribute("aria-hidden");
            dots.forEach(function (dot, i) {
                dot.setAttribute("aria-current", i === index ? "true" : "false");
            });
            if (current) current.textContent = pad(index + 1);
            elapsed = 0;
            setProgress(0);
        }

        function frame(ts) {
            if (lastTs === null) lastTs = ts;
            var dt = ts - lastTs;
            lastTs = ts;
            if (!isPaused()) {
                elapsed += dt;
                if (elapsed >= interval) go(index + 1);
                else setProgress(elapsed / interval);
            }
            window.requestAnimationFrame(frame);
        }

        // Controls
        var prev = hero.querySelector("[data-hero-prev]");
        var next = hero.querySelector("[data-hero-next]");
        if (prev) prev.addEventListener("click", function () { go(index - 1); });
        if (next) next.addEventListener("click", function () { go(index + 1); });
        dots.forEach(function (dot, i) {
            dot.addEventListener("click", function () { go(i); });
        });
        if (toggle) {
            toggle.addEventListener("click", function () {
                userPaused = !userPaused;
                syncPausedState();
            });
        }

        // Pause on hover / when the tab is hidden.
        hero.addEventListener("mouseenter", function () { hoverPaused = true; syncPausedState(); });
        hero.addEventListener("mouseleave", function () { hoverPaused = false; syncPausedState(); });
        document.addEventListener("visibilitychange", function () {
            hiddenPaused = document.hidden;
            lastTs = null;
            syncPausedState();
        });

        // Keyboard arrows while focus is inside the hero.
        hero.addEventListener("keydown", function (e) {
            if (e.key === "ArrowLeft") { e.preventDefault(); go(index - 1); }
            else if (e.key === "ArrowRight") { e.preventDefault(); go(index + 1); }
        });

        // Touch swipe on the image area.
        var startX = null, startY = null;
        media.addEventListener("touchstart", function (e) {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }, { passive: true });
        media.addEventListener("touchend", function (e) {
            if (startX === null) return;
            var dx = e.changedTouches[0].clientX - startX;
            var dy = e.changedTouches[0].clientY - startY;
            if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) go(dx < 0 ? index + 1 : index - 1);
            startX = startY = null;
        }, { passive: true });

        syncPausedState();
        window.requestAnimationFrame(frame);
    }

    /* ------------------------------------------------------------ */
    /* Fader — simple auto crossfade for banner images              */
    /* ------------------------------------------------------------ */
    function initFaders() {
        $all("[data-fader]").forEach(function (root) {
            var items = $all("[data-fader-item]", root);
            if (items.length < 2 || reduceMotion.matches) return;
            var i = 0;
            window.setInterval(function () {
                if (document.hidden) return;
                items[i].classList.remove("is-active");
                i = (i + 1) % items.length;
                items[i].loading = "eager";
                items[i].classList.add("is-active");
            }, 5000);
        });
    }

    /* ------------------------------------------------------------ */
    /* Tabs                                                         */
    /* ------------------------------------------------------------ */
    function initTabs() {
        $all("[data-tabs]").forEach(function (root) {
            var tabs = $all("[role='tab']", root).filter(function (t) {
                return t.closest("[data-tabs]") === root;
            });
            function select(tab, focus) {
                tabs.forEach(function (t) {
                    var on = t === tab;
                    t.setAttribute("aria-selected", on ? "true" : "false");
                    t.tabIndex = on ? 0 : -1;
                    var panel = document.getElementById(t.getAttribute("aria-controls"));
                    if (panel) panel.hidden = !on;
                });
                if (focus) tab.focus();
            }
            tabs.forEach(function (tab, i) {
                tab.addEventListener("click", function () { select(tab, false); });
                tab.addEventListener("keydown", function (e) {
                    var n = null;
                    if (e.key === "ArrowRight") n = tabs[(i + 1) % tabs.length];
                    if (e.key === "ArrowLeft") n = tabs[(i - 1 + tabs.length) % tabs.length];
                    if (e.key === "Home") n = tabs[0];
                    if (e.key === "End") n = tabs[tabs.length - 1];
                    if (n) { e.preventDefault(); select(n, true); }
                });
            });
        });
    }

    /* ------------------------------------------------------------ */
    /* Filters                                                      */
    /* ------------------------------------------------------------ */
    function initFilters() {
        $all("[data-filter]").forEach(function (group) {
            var target = document.getElementById(group.getAttribute("data-filter"));
            if (!target) return;
            var buttons = $all("[data-filter-value]", group);
            buttons.forEach(function (btn) {
                btn.addEventListener("click", function () {
                    var value = btn.getAttribute("data-filter-value");
                    buttons.forEach(function (b) {
                        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
                    });
                    $all("[data-filter-item]", target).forEach(function (item) {
                        var cats = (item.getAttribute("data-filter-item") || "").split(" ");
                        item.hidden = value !== "all" && cats.indexOf(value) === -1;
                    });
                });
            });
        });
    }

    /* ------------------------------------------------------------ */
    /* Lightbox                                                     */
    /* ------------------------------------------------------------ */
    function initLightbox() {
        var box = document.querySelector("[data-lightbox-root]");
        var triggers = $all("[data-lightbox]");
        if (!box || !triggers.length) return;
        var img = box.querySelector("[data-lightbox-img]");
        var caption = box.querySelector("[data-lightbox-caption]");
        var counter = box.querySelector("[data-lightbox-counter]");
        var items = [], index = 0, lastFocus = null;

        function visibleGroup(group) {
            return triggers.filter(function (t) {
                return t.getAttribute("data-lightbox") === group && !t.closest("[hidden]") && !t.hidden;
            });
        }

        function show(i) {
            index = (i + items.length) % items.length;
            var t = items[index];
            img.src = t.getAttribute("href") || t.getAttribute("data-src");
            img.alt = t.getAttribute("data-caption") || "";
            caption.textContent = t.getAttribute("data-caption") || "";
            if (counter) counter.textContent = index + 1 + " / " + items.length;
        }

        function open(trigger) {
            items = visibleGroup(trigger.getAttribute("data-lightbox"));
            lastFocus = trigger;
            box.hidden = false;
            document.documentElement.style.overflow = "hidden";
            show(items.indexOf(trigger));
            box.querySelector("[data-lightbox-close]").focus();
        }

        function close() {
            box.hidden = true;
            img.src = "";
            document.documentElement.style.overflow = "";
            if (lastFocus) lastFocus.focus();
        }

        triggers.forEach(function (t) {
            t.addEventListener("click", function (e) { e.preventDefault(); open(t); });
        });
        box.querySelector("[data-lightbox-close]").addEventListener("click", close);
        box.querySelector("[data-lightbox-prev]").addEventListener("click", function () { show(index - 1); });
        box.querySelector("[data-lightbox-next]").addEventListener("click", function () { show(index + 1); });
        box.addEventListener("click", function (e) { if (e.target === box) close(); });
        document.addEventListener("keydown", function (e) {
            if (box.hidden) return;
            if (e.key === "Escape") close();
            if (e.key === "ArrowLeft") show(index - 1);
            if (e.key === "ArrowRight") show(index + 1);
        });
    }

    /* ------------------------------------------------------------ */
    /* Back to top                                                  */
    /* ------------------------------------------------------------ */
    function initBackToTop() {
        var btn = document.querySelector("[data-back-to-top]");
        if (!btn) return;
        window.addEventListener("scroll", function () {
            btn.classList.toggle("is-visible", window.scrollY > 600);
        }, { passive: true });
        btn.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: reduceMotion.matches ? "auto" : "smooth" });
        });
    }

    onReady(function () {
        initHeader();
        initDrawer();
        initReveal();
        initCountUp();
        initHero();
        initFaders();
        initTabs();
        initFilters();
        initLightbox();
        initBackToTop();
    });
})();
