(() => {
    var Ke = !1,
      ze = !1,
      X = [];
    function St(e) {
      Vr(e);
    }
    function Vr(e) {
      X.includes(e) || X.push(e), Br();
    }
    function Br() {
      !ze && !Ke && ((Ke = !0), queueMicrotask(Hr));
    }
    function Hr() {
      (Ke = !1), (ze = !0);
      for (let e = 0; e < X.length; e++) X[e]();
      (X.length = 0), (ze = !1);
    }
    var w,
      M,
      U,
      Ve,
      Be = !0;
    function At(e) {
      (Be = !1), e(), (Be = !0);
    }
    function Ot(e) {
      (w = e.reactive),
        (U = e.release),
        (M = (t) =>
          e.effect(t, {
            scheduler: (r) => {
              Be ? St(r) : r();
            },
          })),
        (Ve = e.raw);
    }
    function He(e) {
      M = e;
    }
    function Tt(e) {
      let t = () => {};
      return [
        (n) => {
          let i = M(n);
          e._x_effects ||
            ((e._x_effects = new Set()),
            (e._x_runEffects = () => {
              e._x_effects.forEach((o) => o());
            })),
            e._x_effects.add(i),
            (t = () => {
              i !== void 0 && (e._x_effects.delete(i), U(i));
            });
        },
        () => {
          t();
        },
      ];
    }
    var Ct = [],
      Rt = [],
      Mt = [];
    function Nt(e) {
      Mt.push(e);
    }
    function kt(e) {
      Rt.push(e);
    }
    function Dt(e) {
      Ct.push(e);
    }
    function Pt(e, t, r) {
      e._x_attributeCleanups || (e._x_attributeCleanups = {}),
        e._x_attributeCleanups[t] || (e._x_attributeCleanups[t] = []),
        e._x_attributeCleanups[t].push(r);
    }
    function qe(e, t) {
      !e._x_attributeCleanups ||
        Object.entries(e._x_attributeCleanups).forEach(([r, n]) => {
          (t === void 0 || t.includes(r)) &&
            (n.forEach((i) => i()), delete e._x_attributeCleanups[r]);
        });
    }
    var We = new MutationObserver(Ue),
      Ge = !1;
    function Ye() {
      We.observe(document, {
        subtree: !0,
        childList: !0,
        attributes: !0,
        attributeOldValue: !0,
      }),
        (Ge = !0);
    }
    function Ur() {
      qr(), We.disconnect(), (Ge = !1);
    }
    var ee = [],
      Je = !1;
    function qr() {
      (ee = ee.concat(We.takeRecords())),
        ee.length &&
          !Je &&
          ((Je = !0),
          queueMicrotask(() => {
            Wr(), (Je = !1);
          }));
    }
    function Wr() {
      Ue(ee), (ee.length = 0);
    }
    function h(e) {
      if (!Ge) return e();
      Ur();
      let t = e();
      return Ye(), t;
    }
    var Ze = !1,
      me = [];
    function It() {
      Ze = !0;
    }
    function Lt() {
      (Ze = !1), Ue(me), (me = []);
    }
    function Ue(e) {
      if (Ze) {
        me = me.concat(e);
        return;
      }
      let t = [],
        r = [],
        n = new Map(),
        i = new Map();
      for (let o = 0; o < e.length; o++)
        if (
          !e[o].target._x_ignoreMutationObserver &&
          (e[o].type === "childList" &&
            (e[o].addedNodes.forEach((s) => s.nodeType === 1 && t.push(s)),
            e[o].removedNodes.forEach((s) => s.nodeType === 1 && r.push(s))),
          e[o].type === "attributes")
        ) {
          let s = e[o].target,
            a = e[o].attributeName,
            c = e[o].oldValue,
            l = () => {
              n.has(s) || n.set(s, []),
                n.get(s).push({ name: a, value: s.getAttribute(a) });
            },
            u = () => {
              i.has(s) || i.set(s, []), i.get(s).push(a);
            };
          s.hasAttribute(a) && c === null
            ? l()
            : s.hasAttribute(a)
            ? (u(), l())
            : u();
        }
      i.forEach((o, s) => {
        qe(s, o);
      }),
        n.forEach((o, s) => {
          Ct.forEach((a) => a(s, o));
        });
      for (let o of t) r.includes(o) || Mt.forEach((s) => s(o));
      for (let o of r) t.includes(o) || Rt.forEach((s) => s(o));
      (t = null), (r = null), (n = null), (i = null);
    }
    function W(e, t, r) {
      return (
        (e._x_dataStack = [t, ...F(r || e)]),
        () => {
          e._x_dataStack = e._x_dataStack.filter((n) => n !== t);
        }
      );
    }
    function Qe(e, t) {
      let r = e._x_dataStack[0];
      Object.entries(t).forEach(([n, i]) => {
        r[n] = i;
      });
    }
    function F(e) {
      return e._x_dataStack
        ? e._x_dataStack
        : typeof ShadowRoot == "function" && e instanceof ShadowRoot
        ? F(e.host)
        : e.parentNode
        ? F(e.parentNode)
        : [];
    }
    function N(e) {
      let t = new Proxy(
        {},
        {
          ownKeys: () => Array.from(new Set(e.flatMap((r) => Object.keys(r)))),
          has: (r, n) => e.some((i) => i.hasOwnProperty(n)),
          get: (r, n) =>
            (e.find((i) => {
              if (i.hasOwnProperty(n)) {
                let o = Object.getOwnPropertyDescriptor(i, n);
                if (
                  (o.get && o.get._x_alreadyBound) ||
                  (o.set && o.set._x_alreadyBound)
                )
                  return !0;
                if ((o.get || o.set) && o.enumerable) {
                  let s = o.get,
                    a = o.set,
                    c = o;
                  (s = s && s.bind(t)),
                    (a = a && a.bind(t)),
                    s && (s._x_alreadyBound = !0),
                    a && (a._x_alreadyBound = !0),
                    Object.defineProperty(i, n, { ...c, get: s, set: a });
                }
                return !0;
              }
              return !1;
            }) || {})[n],
          set: (r, n, i) => {
            let o = e.find((s) => s.hasOwnProperty(n));
            return o ? (o[n] = i) : (e[e.length - 1][n] = i), !0;
          },
        },
      );
      return t;
    }
    function he(e) {
      let t = (n) => typeof n == "object" && !Array.isArray(n) && n !== null,
        r = (n, i = "") => {
          Object.entries(Object.getOwnPropertyDescriptors(n)).forEach(
            ([o, { value: s, enumerable: a }]) => {
              if (a === !1 || s === void 0) return;
              let c = i === "" ? o : `${i}.${o}`;
              typeof s == "object" && s !== null && s._x_interceptor
                ? (n[o] = s.initialize(e, c, o))
                : t(s) && s !== n && !(s instanceof Element) && r(s, c);
            },
          );
        };
      return r(e);
    }
    function ge(e, t = () => {}) {
      let r = {
        initialValue: void 0,
        _x_interceptor: !0,
        initialize(n, i, o) {
          return e(
            this.initialValue,
            () => Gr(n, i),
            (s) => Xe(n, i, s),
            i,
            o,
          );
        },
      };
      return (
        t(r),
        (n) => {
          if (typeof n == "object" && n !== null && n._x_interceptor) {
            let i = r.initialize.bind(r);
            r.initialize = (o, s, a) => {
              let c = n.initialize(o, s, a);
              return (r.initialValue = c), i(o, s, a);
            };
          } else r.initialValue = n;
          return r;
        }
      );
    }
    function Gr(e, t) {
      return t.split(".").reduce((r, n) => r[n], e);
    }
    function Xe(e, t, r) {
      if ((typeof t == "string" && (t = t.split(".")), t.length === 1))
        e[t[0]] = r;
      else {
        if (t.length === 0) throw error;
        return e[t[0]] || (e[t[0]] = {}), Xe(e[t[0]], t.slice(1), r);
      }
    }
    var $t = {};
    function b(e, t) {
      $t[e] = t;
    }
    function te(e, t) {
      return (
        Object.entries($t).forEach(([r, n]) => {
          Object.defineProperty(e, `$${r}`, {
            get() {
              return n(t, { Alpine: S, interceptor: ge });
            },
            enumerable: !1,
          });
        }),
        e
      );
    }
    function jt(e, t, r, ...n) {
      try {
        return r(...n);
      } catch (i) {
        G(i, e, t);
      }
    }
    function G(e, t, r = void 0) {
      Object.assign(e, { el: t, expression: r }),
        console.warn(
          `Alpine Expression Error: ${e.message}
  
  ${
    r
      ? 'Expression: "' +
        r +
        `"
  
  `
      : ""
  }`,
          t,
        ),
        setTimeout(() => {
          throw e;
        }, 0);
    }
    function v(e, t, r = {}) {
      let n;
      return m(e, t)((i) => (n = i), r), n;
    }
    function m(...e) {
      return Ft(...e);
    }
    var Ft = et;
    function Kt(e) {
      Ft = e;
    }
    function et(e, t) {
      let r = {};
      te(r, e);
      let n = [r, ...F(e)];
      if (typeof t == "function") return Yr(n, t);
      let i = Jr(n, t, e);
      return jt.bind(null, e, t, i);
    }
    function Yr(e, t) {
      return (r = () => {}, { scope: n = {}, params: i = [] } = {}) => {
        let o = t.apply(N([n, ...e]), i);
        _e(r, o);
      };
    }
    var tt = {};
    function Zr(e, t) {
      if (tt[e]) return tt[e];
      let r = Object.getPrototypeOf(async function () {}).constructor,
        n =
          /^[\n\s]*if.*\(.*\)/.test(e) || /^(let|const)\s/.test(e)
            ? `(() => { ${e} })()`
            : e,
        o = (() => {
          try {
            return new r(
              ["__self", "scope"],
              `with (scope) { __self.result = ${n} }; __self.finished = true; return __self.result;`,
            );
          } catch (s) {
            return G(s, t, e), Promise.resolve();
          }
        })();
      return (tt[e] = o), o;
    }
    function Jr(e, t, r) {
      let n = Zr(t, r);
      return (i = () => {}, { scope: o = {}, params: s = [] } = {}) => {
        (n.result = void 0), (n.finished = !1);
        let a = N([o, ...e]);
        if (typeof n == "function") {
          let c = n(n, a).catch((l) => G(l, r, t));
          n.finished
            ? _e(i, n.result, a, s, r)
            : c
                .then((l) => {
                  _e(i, l, a, s, r);
                })
                .catch((l) => G(l, r, t));
        }
      };
    }
    function _e(e, t, r, n, i) {
      if (typeof t == "function") {
        let o = t.apply(r, n);
        o instanceof Promise
          ? o.then((s) => _e(e, s, r, n)).catch((s) => G(s, i, t))
          : e(o);
      } else e(t);
    }
    var rt = "x-";
    function A(e = "") {
      return rt + e;
    }
    function zt(e) {
      rt = e;
    }
    var Vt = {};
    function p(e, t) {
      Vt[e] = t;
    }
    function re(e, t, r) {
      let n = {};
      return Array.from(t)
        .map(Bt((o, s) => (n[o] = s)))
        .filter(Ht)
        .map(Xr(n, r))
        .sort(en)
        .map((o) => Qr(e, o));
    }
    function qt(e) {
      return Array.from(e)
        .map(Bt())
        .filter((t) => !Ht(t));
    }
    var nt = !1,
      ne = new Map(),
      Ut = Symbol();
    function Wt(e) {
      nt = !0;
      let t = Symbol();
      (Ut = t), ne.set(t, []);
      let r = () => {
          for (; ne.get(t).length; ) ne.get(t).shift()();
          ne.delete(t);
        },
        n = () => {
          (nt = !1), r();
        };
      e(r), n();
    }
    function Qr(e, t) {
      let r = () => {},
        n = Vt[t.type] || r,
        i = [],
        o = (d) => i.push(d),
        [s, a] = Tt(e);
      i.push(a);
      let c = {
          Alpine: S,
          effect: s,
          cleanup: o,
          evaluateLater: m.bind(m, e),
          evaluate: v.bind(v, e),
        },
        l = () => i.forEach((d) => d());
      Pt(e, t.original, l);
      let u = () => {
        e._x_ignore ||
          e._x_ignoreSelf ||
          (n.inline && n.inline(e, t, c),
          (n = n.bind(n, e, t, c)),
          nt ? ne.get(Ut).push(n) : n());
      };
      return (u.runCleanups = l), u;
    }
    var ye =
        (e, t) =>
        ({ name: r, value: n }) => (
          r.startsWith(e) && (r = r.replace(e, t)), { name: r, value: n }
        ),
      xe = (e) => e;
    function Bt(e = () => {}) {
      return ({ name: t, value: r }) => {
        let { name: n, value: i } = Gt.reduce((o, s) => s(o), {
          name: t,
          value: r,
        });
        return n !== t && e(n, t), { name: n, value: i };
      };
    }
    var Gt = [];
    function Y(e) {
      Gt.push(e);
    }
    function Ht({ name: e }) {
      return Yt().test(e);
    }
    var Yt = () => new RegExp(`^${rt}([^:^.]+)\\b`);
    function Xr(e, t) {
      return ({ name: r, value: n }) => {
        let i = r.match(Yt()),
          o = r.match(/:([a-zA-Z0-9\-:]+)/),
          s = r.match(/\.[^.\]]+(?=[^\]]*$)/g) || [],
          a = t || e[r] || r;
        return {
          type: i ? i[1] : null,
          value: o ? o[1] : null,
          modifiers: s.map((c) => c.replace(".", "")),
          expression: n,
          original: a,
        };
      };
    }
    var it = "DEFAULT",
      be = [
        "ignore",
        "ref",
        "data",
        "bind",
        "init",
        "for",
        "model",
        "transition",
        "show",
        "if",
        it,
        "element",
      ];
    function en(e, t) {
      let r = be.indexOf(e.type) === -1 ? it : e.type,
        n = be.indexOf(t.type) === -1 ? it : t.type;
      return be.indexOf(r) - be.indexOf(n);
    }
    function K(e, t, r = {}) {
      e.dispatchEvent(
        new CustomEvent(t, {
          detail: r,
          bubbles: !0,
          composed: !0,
          cancelable: !0,
        }),
      );
    }
    var ot = [],
      st = !1;
    function J(e) {
      ot.push(e),
        queueMicrotask(() => {
          st ||
            setTimeout(() => {
              ve();
            });
        });
    }
    function ve() {
      for (st = !1; ot.length; ) ot.shift()();
    }
    function Jt() {
      st = !0;
    }
    function D(e, t) {
      if (typeof ShadowRoot == "function" && e instanceof ShadowRoot) {
        Array.from(e.children).forEach((i) => D(i, t));
        return;
      }
      let r = !1;
      if ((t(e, () => (r = !0)), r)) return;
      let n = e.firstElementChild;
      for (; n; ) D(n, t, !1), (n = n.nextElementSibling);
    }
    function we(e, ...t) {
      console.warn(`Alpine Warning: ${e}`, ...t);
    }
    function Qt() {
      document.body ||
        we(
          "Unable to initialize. Trying to load Alpine before `<body>` is available. Did you forget to add `defer` in Alpine's `<script>` tag?",
        ),
        K(document, "alpine:init"),
        K(document, "alpine:initializing"),
        Ye(),
        Nt((t) => O(t, D)),
        kt((t) => J(() => tn(t))),
        Dt((t, r) => {
          re(t, r).forEach((n) => n());
        });
      let e = (t) => !P(t.parentElement, !0);
      Array.from(document.querySelectorAll(Zt()))
        .filter(e)
        .forEach((t) => {
          O(t);
        }),
        K(document, "alpine:initialized");
    }
    var at = [],
      Xt = [];
    function er() {
      return at.map((e) => e());
    }
    function Zt() {
      return at.concat(Xt).map((e) => e());
    }
    function Ee(e) {
      at.push(e);
    }
    function tr(e) {
      Xt.push(e);
    }
    function P(e, t = !1) {
      if (!e) return;
      if ((t ? Zt() : er()).some((n) => e.matches(n))) return e;
      if (!!e.parentElement) return P(e.parentElement, t);
    }
    function rr(e) {
      return er().some((t) => e.matches(t));
    }
    function O(e, t = D) {
      Wt(() => {
        t(e, (r, n) => {
          re(r, r.attributes).forEach((i) => i()), r._x_ignore && n();
        });
      });
    }
    function tn(e) {
      D(e, (t) => qe(t));
    }
    function ie(e, t) {
      return Array.isArray(t)
        ? nr(e, t.join(" "))
        : typeof t == "object" && t !== null
        ? rn(e, t)
        : typeof t == "function"
        ? ie(e, t())
        : nr(e, t);
    }
    function nr(e, t) {
      let r = (o) => o.split(" ").filter(Boolean),
        n = (o) =>
          o
            .split(" ")
            .filter((s) => !e.classList.contains(s))
            .filter(Boolean),
        i = (o) => (
          e.classList.add(...o),
          () => {
            e.classList.remove(...o);
          }
        );
      return (t = t === !0 ? (t = "") : t || ""), i(n(t));
    }
    function rn(e, t) {
      let r = (a) => a.split(" ").filter(Boolean),
        n = Object.entries(t)
          .flatMap(([a, c]) => (c ? r(a) : !1))
          .filter(Boolean),
        i = Object.entries(t)
          .flatMap(([a, c]) => (c ? !1 : r(a)))
          .filter(Boolean),
        o = [],
        s = [];
      return (
        i.forEach((a) => {
          e.classList.contains(a) && (e.classList.remove(a), s.push(a));
        }),
        n.forEach((a) => {
          e.classList.contains(a) || (e.classList.add(a), o.push(a));
        }),
        () => {
          s.forEach((a) => e.classList.add(a)),
            o.forEach((a) => e.classList.remove(a));
        }
      );
    }
    function z(e, t) {
      return typeof t == "object" && t !== null ? nn(e, t) : on(e, t);
    }
    function nn(e, t) {
      let r = {};
      return (
        Object.entries(t).forEach(([n, i]) => {
          (r[n] = e.style[n]), e.style.setProperty(sn(n), i);
        }),
        setTimeout(() => {
          e.style.length === 0 && e.removeAttribute("style");
        }),
        () => {
          z(e, r);
        }
      );
    }
    function on(e, t) {
      let r = e.getAttribute("style", t);
      return (
        e.setAttribute("style", t),
        () => {
          e.setAttribute("style", r);
        }
      );
    }
    function sn(e) {
      return e.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase();
    }
    function oe(e, t = () => {}) {
      let r = !1;
      return function () {
        r ? t.apply(this, arguments) : ((r = !0), e.apply(this, arguments));
      };
    }
    p(
      "transition",
      (e, { value: t, modifiers: r, expression: n }, { evaluate: i }) => {
        typeof n == "function" && (n = i(n)), n ? an(e, n, t) : cn(e, r, t);
      },
    );
    function an(e, t, r) {
      ir(e, ie, ""),
        {
          enter: (i) => {
            e._x_transition.enter.during = i;
          },
          "enter-start": (i) => {
            e._x_transition.enter.start = i;
          },
          "enter-end": (i) => {
            e._x_transition.enter.end = i;
          },
          leave: (i) => {
            e._x_transition.leave.during = i;
          },
          "leave-start": (i) => {
            e._x_transition.leave.start = i;
          },
          "leave-end": (i) => {
            e._x_transition.leave.end = i;
          },
        }[r](t);
    }
    function cn(e, t, r) {
      ir(e, z);
      let n = !t.includes("in") && !t.includes("out") && !r,
        i = n || t.includes("in") || ["enter"].includes(r),
        o = n || t.includes("out") || ["leave"].includes(r);
      t.includes("in") && !n && (t = t.filter((_, x) => x < t.indexOf("out"))),
        t.includes("out") && !n && (t = t.filter((_, x) => x > t.indexOf("out")));
      let s = !t.includes("opacity") && !t.includes("scale"),
        a = s || t.includes("opacity"),
        c = s || t.includes("scale"),
        l = a ? 0 : 1,
        u = c ? se(t, "scale", 95) / 100 : 1,
        d = se(t, "delay", 0),
        y = se(t, "origin", "center"),
        C = "opacity, transform",
        H = se(t, "duration", 150) / 1e3,
        de = se(t, "duration", 75) / 1e3,
        f = "cubic-bezier(0.4, 0.0, 0.2, 1)";
      i &&
        ((e._x_transition.enter.during = {
          transformOrigin: y,
          transitionDelay: d,
          transitionProperty: C,
          transitionDuration: `${H}s`,
          transitionTimingFunction: f,
        }),
        (e._x_transition.enter.start = { opacity: l, transform: `scale(${u})` }),
        (e._x_transition.enter.end = { opacity: 1, transform: "scale(1)" })),
        o &&
          ((e._x_transition.leave.during = {
            transformOrigin: y,
            transitionDelay: d,
            transitionProperty: C,
            transitionDuration: `${de}s`,
            transitionTimingFunction: f,
          }),
          (e._x_transition.leave.start = { opacity: 1, transform: "scale(1)" }),
          (e._x_transition.leave.end = { opacity: l, transform: `scale(${u})` }));
    }
    function ir(e, t, r = {}) {
      e._x_transition ||
        (e._x_transition = {
          enter: { during: r, start: r, end: r },
          leave: { during: r, start: r, end: r },
          in(n = () => {}, i = () => {}) {
            Se(
              e,
              t,
              {
                during: this.enter.during,
                start: this.enter.start,
                end: this.enter.end,
              },
              n,
              i,
            );
          },
          out(n = () => {}, i = () => {}) {
            Se(
              e,
              t,
              {
                during: this.leave.during,
                start: this.leave.start,
                end: this.leave.end,
              },
              n,
              i,
            );
          },
        });
    }
    window.Element.prototype._x_toggleAndCascadeWithTransitions = function (
      e,
      t,
      r,
      n,
    ) {
      let i = () => {
        document.visibilityState === "visible"
          ? requestAnimationFrame(r)
          : setTimeout(r);
      };
      if (t) {
        e._x_transition && (e._x_transition.enter || e._x_transition.leave)
          ? e._x_transition.enter &&
            (Object.entries(e._x_transition.enter.during).length ||
              Object.entries(e._x_transition.enter.start).length ||
              Object.entries(e._x_transition.enter.end).length)
            ? e._x_transition.in(r)
            : i()
          : e._x_transition
          ? e._x_transition.in(r)
          : i();
        return;
      }
      (e._x_hidePromise = e._x_transition
        ? new Promise((o, s) => {
            e._x_transition.out(
              () => {},
              () => o(n),
            ),
              e._x_transitioning.beforeCancel(() =>
                s({ isFromCancelledTransition: !0 }),
              );
          })
        : Promise.resolve(n)),
        queueMicrotask(() => {
          let o = or(e);
          o
            ? (o._x_hideChildren || (o._x_hideChildren = []),
              o._x_hideChildren.push(e))
            : queueMicrotask(() => {
                let s = (a) => {
                  let c = Promise.all([
                    a._x_hidePromise,
                    ...(a._x_hideChildren || []).map(s),
                  ]).then(([l]) => l());
                  return delete a._x_hidePromise, delete a._x_hideChildren, c;
                };
                s(e).catch((a) => {
                  if (!a.isFromCancelledTransition) throw a;
                });
              });
        });
    };
    function or(e) {
      let t = e.parentNode;
      if (!!t) return t._x_hidePromise ? t : or(t);
    }
    function Se(
      e,
      t,
      { during: r, start: n, end: i } = {},
      o = () => {},
      s = () => {},
    ) {
      if (
        (e._x_transitioning && e._x_transitioning.cancel(),
        Object.keys(r).length === 0 &&
          Object.keys(n).length === 0 &&
          Object.keys(i).length === 0)
      ) {
        o(), s();
        return;
      }
      let a, c, l;
      ln(e, {
        start() {
          a = t(e, n);
        },
        during() {
          c = t(e, r);
        },
        before: o,
        end() {
          a(), (l = t(e, i));
        },
        after: s,
        cleanup() {
          c(), l();
        },
      });
    }
    function ln(e, t) {
      let r,
        n,
        i,
        o = oe(() => {
          h(() => {
            (r = !0),
              n || t.before(),
              i || (t.end(), ve()),
              t.after(),
              e.isConnected && t.cleanup(),
              delete e._x_transitioning;
          });
        });
      (e._x_transitioning = {
        beforeCancels: [],
        beforeCancel(s) {
          this.beforeCancels.push(s);
        },
        cancel: oe(function () {
          for (; this.beforeCancels.length; ) this.beforeCancels.shift()();
          o();
        }),
        finish: o,
      }),
        h(() => {
          t.start(), t.during();
        }),
        Jt(),
        requestAnimationFrame(() => {
          if (r) return;
          let s =
              Number(
                getComputedStyle(e)
                  .transitionDuration.replace(/,.*/, "")
                  .replace("s", ""),
              ) * 1e3,
            a =
              Number(
                getComputedStyle(e)
                  .transitionDelay.replace(/,.*/, "")
                  .replace("s", ""),
              ) * 1e3;
          s === 0 &&
            (s =
              Number(getComputedStyle(e).animationDuration.replace("s", "")) *
              1e3),
            h(() => {
              t.before();
            }),
            (n = !0),
            requestAnimationFrame(() => {
              r ||
                (h(() => {
                  t.end();
                }),
                ve(),
                setTimeout(e._x_transitioning.finish, s + a),
                (i = !0));
            });
        });
    }
    function se(e, t, r) {
      if (e.indexOf(t) === -1) return r;
      let n = e[e.indexOf(t) + 1];
      if (!n || (t === "scale" && isNaN(n))) return r;
      if (t === "duration") {
        let i = n.match(/([0-9]+)ms/);
        if (i) return i[1];
      }
      return t === "origin" &&
        ["top", "right", "left", "center", "bottom"].includes(e[e.indexOf(t) + 2])
        ? [n, e[e.indexOf(t) + 2]].join(" ")
        : n;
    }
    function Ae(e, t) {
      var r;
      return function () {
        var n = this,
          i = arguments,
          o = function () {
            (r = null), e.apply(n, i);
          };
        clearTimeout(r), (r = setTimeout(o, t));
      };
    }
    function Oe(e, t) {
      let r;
      return function () {
        let n = this,
          i = arguments;
        r || (e.apply(n, i), (r = !0), setTimeout(() => (r = !1), t));
      };
    }
    function sr(e) {
      e(S);
    }
    var V = {},
      ar = !1;
    function cr(e, t) {
      if ((ar || ((V = w(V)), (ar = !0)), t === void 0)) return V[e];
      (V[e] = t),
        typeof t == "object" &&
          t !== null &&
          t.hasOwnProperty("init") &&
          typeof t.init == "function" &&
          V[e].init(),
        he(V[e]);
    }
    function lr() {
      return V;
    }
    var ct = !1;
    function I(e, t = () => {}) {
      return (...r) => (ct ? t(...r) : e(...r));
    }
    function ur(e, t) {
      (t._x_dataStack = e._x_dataStack),
        (ct = !0),
        fn(() => {
          un(t);
        }),
        (ct = !1);
    }
    function un(e) {
      let t = !1;
      O(e, (n, i) => {
        D(n, (o, s) => {
          if (t && rr(o)) return s();
          (t = !0), i(o, s);
        });
      });
    }
    function fn(e) {
      let t = M;
      He((r, n) => {
        let i = t(r);
        return U(i), () => {};
      }),
        e(),
        He(t);
    }
    var fr = {};
    function dr(e, t) {
      fr[e] = t;
    }
    function pr(e, t) {
      return (
        Object.entries(fr).forEach(([r, n]) => {
          Object.defineProperty(e, r, {
            get() {
              return (...i) => n.bind(t)(...i);
            },
            enumerable: !1,
          });
        }),
        e
      );
    }
    var dn = {
        get reactive() {
          return w;
        },
        get release() {
          return U;
        },
        get effect() {
          return M;
        },
        get raw() {
          return Ve;
        },
        version: "3.5.1",
        flushAndStopDeferringMutations: Lt,
        disableEffectScheduling: At,
        setReactivityEngine: Ot,
        skipDuringClone: I,
        addRootSelector: Ee,
        deferMutations: It,
        mapAttributes: Y,
        evaluateLater: m,
        setEvaluator: Kt,
        mergeProxies: N,
        closestRoot: P,
        interceptor: ge,
        transition: Se,
        setStyles: z,
        mutateDom: h,
        directive: p,
        throttle: Oe,
        debounce: Ae,
        evaluate: v,
        initTree: O,
        nextTick: J,
        prefix: zt,
        plugin: sr,
        magic: b,
        store: cr,
        start: Qt,
        clone: ur,
        data: dr,
      },
      S = dn;
    function lt(e, t) {
      let r = Object.create(null),
        n = e.split(",");
      for (let i = 0; i < n.length; i++) r[n[i]] = !0;
      return t ? (i) => !!r[i.toLowerCase()] : (i) => !!r[i];
    }
    var Ro = {
        [1]: "TEXT",
        [2]: "CLASS",
        [4]: "STYLE",
        [8]: "PROPS",
        [16]: "FULL_PROPS",
        [32]: "HYDRATE_EVENTS",
        [64]: "STABLE_FRAGMENT",
        [128]: "KEYED_FRAGMENT",
        [256]: "UNKEYED_FRAGMENT",
        [512]: "NEED_PATCH",
        [1024]: "DYNAMIC_SLOTS",
        [2048]: "DEV_ROOT_FRAGMENT",
        [-1]: "HOISTED",
        [-2]: "BAIL",
      },
      Mo = { [1]: "STABLE", [2]: "DYNAMIC", [3]: "FORWARDED" };
    var pn =
      "itemscope,allowfullscreen,formnovalidate,ismap,nomodule,novalidate,readonly";
    var No = lt(
      pn +
        ",async,autofocus,autoplay,controls,default,defer,disabled,hidden,loop,open,required,reversed,scoped,seamless,checked,muted,multiple,selected",
    );
    var mr = Object.freeze({}),
      ko = Object.freeze([]);
    var ut = Object.assign;
    var mn = Object.prototype.hasOwnProperty,
      ae = (e, t) => mn.call(e, t),
      L = Array.isArray,
      Z = (e) => hr(e) === "[object Map]";
    var hn = (e) => typeof e == "string",
      Te = (e) => typeof e == "symbol",
      ce = (e) => e !== null && typeof e == "object";
    var gn = Object.prototype.toString,
      hr = (e) => gn.call(e),
      ft = (e) => hr(e).slice(8, -1);
    var Ce = (e) =>
      hn(e) && e !== "NaN" && e[0] !== "-" && "" + parseInt(e, 10) === e;
    var Re = (e) => {
        let t = Object.create(null);
        return (r) => t[r] || (t[r] = e(r));
      },
      _n = /-(\w)/g,
      Do = Re((e) => e.replace(_n, (t, r) => (r ? r.toUpperCase() : ""))),
      yn = /\B([A-Z])/g,
      Po = Re((e) => e.replace(yn, "-$1").toLowerCase()),
      dt = Re((e) => e.charAt(0).toUpperCase() + e.slice(1)),
      Io = Re((e) => (e ? `on${dt(e)}` : "")),
      pt = (e, t) => e !== t && (e === e || t === t);
    var mt = new WeakMap(),
      le = [],
      T,
      B = Symbol("iterate"),
      ht = Symbol("Map key iterate");
    function xn(e) {
      return e && e._isEffect === !0;
    }
    function gr(e, t = mr) {
      xn(e) && (e = e.raw);
      let r = bn(e, t);
      return t.lazy || r(), r;
    }
    function yr(e) {
      e.active &&
        (_r(e), e.options.onStop && e.options.onStop(), (e.active = !1));
    }
    var vn = 0;
    function bn(e, t) {
      let r = function () {
        if (!r.active) return e();
        if (!le.includes(r)) {
          _r(r);
          try {
            return wn(), le.push(r), (T = r), e();
          } finally {
            le.pop(), xr(), (T = le[le.length - 1]);
          }
        }
      };
      return (
        (r.id = vn++),
        (r.allowRecurse = !!t.allowRecurse),
        (r._isEffect = !0),
        (r.active = !0),
        (r.raw = e),
        (r.deps = []),
        (r.options = t),
        r
      );
    }
    function _r(e) {
      let { deps: t } = e;
      if (t.length) {
        for (let r = 0; r < t.length; r++) t[r].delete(e);
        t.length = 0;
      }
    }
    var Q = !0,
      gt = [];
    function En() {
      gt.push(Q), (Q = !1);
    }
    function wn() {
      gt.push(Q), (Q = !0);
    }
    function xr() {
      let e = gt.pop();
      Q = e === void 0 ? !0 : e;
    }
    function E(e, t, r) {
      if (!Q || T === void 0) return;
      let n = mt.get(e);
      n || mt.set(e, (n = new Map()));
      let i = n.get(r);
      i || n.set(r, (i = new Set())),
        i.has(T) ||
          (i.add(T),
          T.deps.push(i),
          T.options.onTrack &&
            T.options.onTrack({ effect: T, target: e, type: t, key: r }));
    }
    function $(e, t, r, n, i, o) {
      let s = mt.get(e);
      if (!s) return;
      let a = new Set(),
        c = (u) => {
          u &&
            u.forEach((d) => {
              (d !== T || d.allowRecurse) && a.add(d);
            });
        };
      if (t === "clear") s.forEach(c);
      else if (r === "length" && L(e))
        s.forEach((u, d) => {
          (d === "length" || d >= n) && c(u);
        });
      else
        switch ((r !== void 0 && c(s.get(r)), t)) {
          case "add":
            L(e)
              ? Ce(r) && c(s.get("length"))
              : (c(s.get(B)), Z(e) && c(s.get(ht)));
            break;
          case "delete":
            L(e) || (c(s.get(B)), Z(e) && c(s.get(ht)));
            break;
          case "set":
            Z(e) && c(s.get(B));
            break;
        }
      let l = (u) => {
        u.options.onTrigger &&
          u.options.onTrigger({
            effect: u,
            target: e,
            key: r,
            type: t,
            newValue: n,
            oldValue: i,
            oldTarget: o,
          }),
          u.options.scheduler ? u.options.scheduler(u) : u();
      };
      a.forEach(l);
    }
    var Sn = lt("__proto__,__v_isRef,__isVue"),
      br = new Set(
        Object.getOwnPropertyNames(Symbol)
          .map((e) => Symbol[e])
          .filter(Te),
      ),
      An = Me(),
      On = Me(!1, !0),
      Tn = Me(!0),
      Cn = Me(!0, !0),
      Ne = {};
    ["includes", "indexOf", "lastIndexOf"].forEach((e) => {
      let t = Array.prototype[e];
      Ne[e] = function (...r) {
        let n = g(this);
        for (let o = 0, s = this.length; o < s; o++) E(n, "get", o + "");
        let i = t.apply(n, r);
        return i === -1 || i === !1 ? t.apply(n, r.map(g)) : i;
      };
    });
    ["push", "pop", "shift", "unshift", "splice"].forEach((e) => {
      let t = Array.prototype[e];
      Ne[e] = function (...r) {
        En();
        let n = t.apply(this, r);
        return xr(), n;
      };
    });
    function Me(e = !1, t = !1) {
      return function (n, i, o) {
        if (i === "__v_isReactive") return !e;
        if (i === "__v_isReadonly") return e;
        if (i === "__v_raw" && o === (e ? (t ? Mn : wr) : t ? Rn : vr).get(n))
          return n;
        let s = L(n);
        if (!e && s && ae(Ne, i)) return Reflect.get(Ne, i, o);
        let a = Reflect.get(n, i, o);
        return (Te(i) ? br.has(i) : Sn(i)) || (e || E(n, "get", i), t)
          ? a
          : _t(a)
          ? !s || !Ce(i)
            ? a.value
            : a
          : ce(a)
          ? e
            ? Er(a)
            : ke(a)
          : a;
      };
    }
    var Nn = Sr(),
      kn = Sr(!0);
    function Sr(e = !1) {
      return function (r, n, i, o) {
        let s = r[n];
        if (!e && ((i = g(i)), (s = g(s)), !L(r) && _t(s) && !_t(i)))
          return (s.value = i), !0;
        let a = L(r) && Ce(n) ? Number(n) < r.length : ae(r, n),
          c = Reflect.set(r, n, i, o);
        return (
          r === g(o) &&
            (a ? pt(i, s) && $(r, "set", n, i, s) : $(r, "add", n, i)),
          c
        );
      };
    }
    function Dn(e, t) {
      let r = ae(e, t),
        n = e[t],
        i = Reflect.deleteProperty(e, t);
      return i && r && $(e, "delete", t, void 0, n), i;
    }
    function Pn(e, t) {
      let r = Reflect.has(e, t);
      return (!Te(t) || !br.has(t)) && E(e, "has", t), r;
    }
    function In(e) {
      return E(e, "iterate", L(e) ? "length" : B), Reflect.ownKeys(e);
    }
    var Ar = { get: An, set: Nn, deleteProperty: Dn, has: Pn, ownKeys: In },
      Or = {
        get: Tn,
        set(e, t) {
          return (
            console.warn(
              `Set operation on key "${String(t)}" failed: target is readonly.`,
              e,
            ),
            !0
          );
        },
        deleteProperty(e, t) {
          return (
            console.warn(
              `Delete operation on key "${String(
                t,
              )}" failed: target is readonly.`,
              e,
            ),
            !0
          );
        },
      },
      zo = ut({}, Ar, { get: On, set: kn }),
      Vo = ut({}, Or, { get: Cn }),
      yt = (e) => (ce(e) ? ke(e) : e),
      xt = (e) => (ce(e) ? Er(e) : e),
      bt = (e) => e,
      De = (e) => Reflect.getPrototypeOf(e);
    function Pe(e, t, r = !1, n = !1) {
      e = e.__v_raw;
      let i = g(e),
        o = g(t);
      t !== o && !r && E(i, "get", t), !r && E(i, "get", o);
      let { has: s } = De(i),
        a = n ? bt : r ? xt : yt;
      if (s.call(i, t)) return a(e.get(t));
      if (s.call(i, o)) return a(e.get(o));
      e !== i && e.get(t);
    }
    function Ie(e, t = !1) {
      let r = this.__v_raw,
        n = g(r),
        i = g(e);
      return (
        e !== i && !t && E(n, "has", e),
        !t && E(n, "has", i),
        e === i ? r.has(e) : r.has(e) || r.has(i)
      );
    }
    function Le(e, t = !1) {
      return (
        (e = e.__v_raw), !t && E(g(e), "iterate", B), Reflect.get(e, "size", e)
      );
    }
    function Tr(e) {
      e = g(e);
      let t = g(this);
      return De(t).has.call(t, e) || (t.add(e), $(t, "add", e, e)), this;
    }
    function Rr(e, t) {
      t = g(t);
      let r = g(this),
        { has: n, get: i } = De(r),
        o = n.call(r, e);
      o ? Cr(r, n, e) : ((e = g(e)), (o = n.call(r, e)));
      let s = i.call(r, e);
      return (
        r.set(e, t),
        o ? pt(t, s) && $(r, "set", e, t, s) : $(r, "add", e, t),
        this
      );
    }
    function Mr(e) {
      let t = g(this),
        { has: r, get: n } = De(t),
        i = r.call(t, e);
      i ? Cr(t, r, e) : ((e = g(e)), (i = r.call(t, e)));
      let o = n ? n.call(t, e) : void 0,
        s = t.delete(e);
      return i && $(t, "delete", e, void 0, o), s;
    }
    function Nr() {
      let e = g(this),
        t = e.size !== 0,
        r = Z(e) ? new Map(e) : new Set(e),
        n = e.clear();
      return t && $(e, "clear", void 0, void 0, r), n;
    }
    function $e(e, t) {
      return function (n, i) {
        let o = this,
          s = o.__v_raw,
          a = g(s),
          c = t ? bt : e ? xt : yt;
        return (
          !e && E(a, "iterate", B), s.forEach((l, u) => n.call(i, c(l), c(u), o))
        );
      };
    }
    function je(e, t, r) {
      return function (...n) {
        let i = this.__v_raw,
          o = g(i),
          s = Z(o),
          a = e === "entries" || (e === Symbol.iterator && s),
          c = e === "keys" && s,
          l = i[e](...n),
          u = r ? bt : t ? xt : yt;
        return (
          !t && E(o, "iterate", c ? ht : B),
          {
            next() {
              let { value: d, done: y } = l.next();
              return y
                ? { value: d, done: y }
                : { value: a ? [u(d[0]), u(d[1])] : u(d), done: y };
            },
            [Symbol.iterator]() {
              return this;
            },
          }
        );
      };
    }
    function j(e) {
      return function (...t) {
        {
          let r = t[0] ? `on key "${t[0]}" ` : "";
          console.warn(
            `${dt(e)} operation ${r}failed: target is readonly.`,
            g(this),
          );
        }
        return e === "delete" ? !1 : this;
      };
    }
    var kr = {
        get(e) {
          return Pe(this, e);
        },
        get size() {
          return Le(this);
        },
        has: Ie,
        add: Tr,
        set: Rr,
        delete: Mr,
        clear: Nr,
        forEach: $e(!1, !1),
      },
      Dr = {
        get(e) {
          return Pe(this, e, !1, !0);
        },
        get size() {
          return Le(this);
        },
        has: Ie,
        add: Tr,
        set: Rr,
        delete: Mr,
        clear: Nr,
        forEach: $e(!1, !0),
      },
      Pr = {
        get(e) {
          return Pe(this, e, !0);
        },
        get size() {
          return Le(this, !0);
        },
        has(e) {
          return Ie.call(this, e, !0);
        },
        add: j("add"),
        set: j("set"),
        delete: j("delete"),
        clear: j("clear"),
        forEach: $e(!0, !1),
      },
      Ir = {
        get(e) {
          return Pe(this, e, !0, !0);
        },
        get size() {
          return Le(this, !0);
        },
        has(e) {
          return Ie.call(this, e, !0);
        },
        add: j("add"),
        set: j("set"),
        delete: j("delete"),
        clear: j("clear"),
        forEach: $e(!0, !0),
      },
      Ln = ["keys", "values", "entries", Symbol.iterator];
    Ln.forEach((e) => {
      (kr[e] = je(e, !1, !1)),
        (Pr[e] = je(e, !0, !1)),
        (Dr[e] = je(e, !1, !0)),
        (Ir[e] = je(e, !0, !0));
    });
    function Fe(e, t) {
      let r = t ? (e ? Ir : Dr) : e ? Pr : kr;
      return (n, i, o) =>
        i === "__v_isReactive"
          ? !e
          : i === "__v_isReadonly"
          ? e
          : i === "__v_raw"
          ? n
          : Reflect.get(ae(r, i) && i in n ? r : n, i, o);
    }
    var $n = { get: Fe(!1, !1) },
      Bo = { get: Fe(!1, !0) },
      jn = { get: Fe(!0, !1) },
      Ho = { get: Fe(!0, !0) };
    function Cr(e, t, r) {
      let n = g(r);
      if (n !== r && t.call(e, n)) {
        let i = ft(e);
        console.warn(
          `Reactive ${i} contains both the raw and reactive versions of the same object${
            i === "Map" ? " as keys" : ""
          }, which can lead to inconsistencies. Avoid differentiating between the raw and reactive versions of an object and only use the reactive version if possible.`,
        );
      }
    }
    var vr = new WeakMap(),
      Rn = new WeakMap(),
      wr = new WeakMap(),
      Mn = new WeakMap();
    function Fn(e) {
      switch (e) {
        case "Object":
        case "Array":
          return 1;
        case "Map":
        case "Set":
        case "WeakMap":
        case "WeakSet":
          return 2;
        default:
          return 0;
      }
    }
    function Kn(e) {
      return e.__v_skip || !Object.isExtensible(e) ? 0 : Fn(ft(e));
    }
    function ke(e) {
      return e && e.__v_isReadonly ? e : Lr(e, !1, Ar, $n, vr);
    }
    function Er(e) {
      return Lr(e, !0, Or, jn, wr);
    }
    function Lr(e, t, r, n, i) {
      if (!ce(e))
        return console.warn(`value cannot be made reactive: ${String(e)}`), e;
      if (e.__v_raw && !(t && e.__v_isReactive)) return e;
      let o = i.get(e);
      if (o) return o;
      let s = Kn(e);
      if (s === 0) return e;
      let a = new Proxy(e, s === 2 ? n : r);
      return i.set(e, a), a;
    }
    function g(e) {
      return (e && g(e.__v_raw)) || e;
    }
    function _t(e) {
      return Boolean(e && e.__v_isRef === !0);
    }
    b("nextTick", () => J);
    b("dispatch", (e) => K.bind(K, e));
    b("watch", (e) => (t, r) => {
      let n = m(e, t),
        i = !0,
        o;
      M(() =>
        n((s) => {
          let a = document.createElement("div");
          (a.dataset.throwAway = s),
            i
              ? (o = s)
              : queueMicrotask(() => {
                  r(s, o), (o = s);
                }),
            (i = !1);
        }),
      );
    });
    b("store", lr);
    b("data", (e) => N(F(e)));
    b("root", (e) => P(e));
    b(
      "refs",
      (e) => (e._x_refs_proxy || (e._x_refs_proxy = N(zn(e))), e._x_refs_proxy),
    );
    function zn(e) {
      let t = [],
        r = e;
      for (; r; ) r._x_refs && t.push(r._x_refs), (r = r.parentNode);
      return t;
    }
    b("el", (e) => e);
    var $r = () => {};
    $r.inline = (e, { modifiers: t }, { cleanup: r }) => {
      t.includes("self") ? (e._x_ignoreSelf = !0) : (e._x_ignore = !0),
        r(() => {
          t.includes("self") ? delete e._x_ignoreSelf : delete e._x_ignore;
        });
    };
    p("ignore", $r);
    p("effect", (e, { expression: t }, { effect: r }) => r(m(e, t)));
    function ue(e, t, r, n = []) {
      switch (
        (e._x_bindings || (e._x_bindings = w({})),
        (e._x_bindings[t] = r),
        (t = n.includes("camel") ? Un(t) : t),
        t)
      ) {
        case "value":
          Vn(e, r);
          break;
        case "style":
          Hn(e, r);
          break;
        case "class":
          Bn(e, r);
          break;
        default:
          qn(e, t, r);
          break;
      }
    }
    function Vn(e, t) {
      if (e.type === "radio")
        e.attributes.value === void 0 && (e.value = t),
          window.fromModel && (e.checked = jr(e.value, t));
      else if (e.type === "checkbox")
        Number.isInteger(t)
          ? (e.value = t)
          : !Number.isInteger(t) &&
            !Array.isArray(t) &&
            typeof t != "boolean" &&
            ![null, void 0].includes(t)
          ? (e.value = String(t))
          : Array.isArray(t)
          ? (e.checked = t.some((r) => jr(r, e.value)))
          : (e.checked = !!t);
      else if (e.tagName === "SELECT") Wn(e, t);
      else {
        if (e.value === t) return;
        e.value = t;
      }
    }
    function Bn(e, t) {
      e._x_undoAddedClasses && e._x_undoAddedClasses(),
        (e._x_undoAddedClasses = ie(e, t));
    }
    function Hn(e, t) {
      e._x_undoAddedStyles && e._x_undoAddedStyles(),
        (e._x_undoAddedStyles = z(e, t));
    }
    function qn(e, t, r) {
      [null, void 0, !1].includes(r) && Jn(t)
        ? e.removeAttribute(t)
        : (Yn(t) && (r = t), Gn(e, t, r));
    }
    function Gn(e, t, r) {
      e.getAttribute(t) != r && e.setAttribute(t, r);
    }
    function Wn(e, t) {
      let r = [].concat(t).map((n) => n + "");
      Array.from(e.options).forEach((n) => {
        n.selected = r.includes(n.value);
      });
    }
    function Un(e) {
      return e.toLowerCase().replace(/-(\w)/g, (t, r) => r.toUpperCase());
    }
    function jr(e, t) {
      return e == t;
    }
    function Yn(e) {
      return [
        "disabled",
        "checked",
        "required",
        "readonly",
        "hidden",
        "open",
        "selected",
        "autofocus",
        "itemscope",
        "multiple",
        "novalidate",
        "allowfullscreen",
        "allowpaymentrequest",
        "formnovalidate",
        "autoplay",
        "controls",
        "loop",
        "muted",
        "playsinline",
        "default",
        "ismap",
        "reversed",
        "async",
        "defer",
        "nomodule",
      ].includes(e);
    }
    function Jn(e) {
      return !["aria-pressed", "aria-checked", "aria-expanded"].includes(e);
    }
    function fe(e, t, r, n) {
      let i = e,
        o = (c) => n(c),
        s = {},
        a = (c, l) => (u) => l(c, u);
      if (
        (r.includes("dot") && (t = Zn(t)),
        r.includes("camel") && (t = Qn(t)),
        r.includes("passive") && (s.passive = !0),
        r.includes("capture") && (s.capture = !0),
        r.includes("window") && (i = window),
        r.includes("document") && (i = document),
        r.includes("prevent") &&
          (o = a(o, (c, l) => {
            l.preventDefault(), c(l);
          })),
        r.includes("stop") &&
          (o = a(o, (c, l) => {
            l.stopPropagation(), c(l);
          })),
        r.includes("self") &&
          (o = a(o, (c, l) => {
            l.target === e && c(l);
          })),
        (r.includes("away") || r.includes("outside")) &&
          ((i = document),
          (o = a(o, (c, l) => {
            e.contains(l.target) ||
              (e.offsetWidth < 1 && e.offsetHeight < 1) ||
              (e._x_isShown !== !1 && c(l));
          }))),
        (o = a(o, (c, l) => {
          (Xn(t) && ei(l, r)) || c(l);
        })),
        r.includes("debounce"))
      ) {
        let c = r[r.indexOf("debounce") + 1] || "invalid-wait",
          l = vt(c.split("ms")[0]) ? Number(c.split("ms")[0]) : 250;
        o = Ae(o, l);
      }
      if (r.includes("throttle")) {
        let c = r[r.indexOf("throttle") + 1] || "invalid-wait",
          l = vt(c.split("ms")[0]) ? Number(c.split("ms")[0]) : 250;
        o = Oe(o, l);
      }
      return (
        r.includes("once") &&
          (o = a(o, (c, l) => {
            c(l), i.removeEventListener(t, o, s);
          })),
        i.addEventListener(t, o, s),
        () => {
          i.removeEventListener(t, o, s);
        }
      );
    }
    function Zn(e) {
      return e.replace(/-/g, ".");
    }
    function Qn(e) {
      return e.toLowerCase().replace(/-(\w)/g, (t, r) => r.toUpperCase());
    }
    function vt(e) {
      return !Array.isArray(e) && !isNaN(e);
    }
    function ti(e) {
      return e
        .replace(/([a-z])([A-Z])/g, "$1-$2")
        .replace(/[_\s]/, "-")
        .toLowerCase();
    }
    function Xn(e) {
      return ["keydown", "keyup"].includes(e);
    }
    function ei(e, t) {
      let r = t.filter(
        (o) => !["window", "document", "prevent", "stop", "once"].includes(o),
      );
      if (r.includes("debounce")) {
        let o = r.indexOf("debounce");
        r.splice(o, vt((r[o + 1] || "invalid-wait").split("ms")[0]) ? 2 : 1);
      }
      if (r.length === 0 || (r.length === 1 && Fr(e.key).includes(r[0])))
        return !1;
      let i = ["ctrl", "shift", "alt", "meta", "cmd", "super"].filter((o) =>
        r.includes(o),
      );
      return (
        (r = r.filter((o) => !i.includes(o))),
        !(
          i.length > 0 &&
          i.filter(
            (s) => ((s === "cmd" || s === "super") && (s = "meta"), e[`${s}Key`]),
          ).length === i.length &&
          Fr(e.key).includes(r[0])
        )
      );
    }
    function Fr(e) {
      if (!e) return [];
      e = ti(e);
      let t = {
        ctrl: "control",
        slash: "/",
        space: "-",
        spacebar: "-",
        cmd: "meta",
        esc: "escape",
        up: "arrow-up",
        down: "arrow-down",
        left: "arrow-left",
        right: "arrow-right",
        period: ".",
        equal: "=",
      };
      return (
        (t[e] = e),
        Object.keys(t)
          .map((r) => {
            if (t[r] === e) return r;
          })
          .filter((r) => r)
      );
    }
    p(
      "model",
      (e, { modifiers: t, expression: r }, { effect: n, cleanup: i }) => {
        let o = m(e, r),
          s = `${r} = rightSideOfExpression($event, ${r})`,
          a = m(e, s);
        var c =
          e.tagName.toLowerCase() === "select" ||
          ["checkbox", "radio"].includes(e.type) ||
          t.includes("lazy")
            ? "change"
            : "input";
        let l = ri(e, t, r),
          u = fe(e, c, t, (y) => {
            a(() => {}, { scope: { $event: y, rightSideOfExpression: l } });
          });
        i(() => u());
        let d = m(e, `${r} = __placeholder`);
        (e._x_model = {
          get() {
            let y;
            return o((C) => (y = C)), y;
          },
          set(y) {
            d(() => {}, { scope: { __placeholder: y } });
          },
        }),
          (e._x_forceModelUpdate = () => {
            o((y) => {
              y === void 0 && r.match(/\./) && (y = ""),
                (window.fromModel = !0),
                h(() => ue(e, "value", y)),
                delete window.fromModel;
            });
          }),
          n(() => {
            (t.includes("unintrusive") && document.activeElement.isSameNode(e)) ||
              e._x_forceModelUpdate();
          });
      },
    );
    function ri(e, t, r) {
      return (
        e.type === "radio" &&
          h(() => {
            e.hasAttribute("name") || e.setAttribute("name", r);
          }),
        (n, i) =>
          h(() => {
            if (n instanceof CustomEvent && n.detail !== void 0)
              return n.detail || n.target.value;
            if (e.type === "checkbox")
              if (Array.isArray(i)) {
                let o = t.includes("number")
                  ? wt(n.target.value)
                  : n.target.value;
                return n.target.checked
                  ? i.concat([o])
                  : i.filter((s) => !ni(s, o));
              } else return n.target.checked;
            else {
              if (e.tagName.toLowerCase() === "select" && e.multiple)
                return t.includes("number")
                  ? Array.from(n.target.selectedOptions).map((o) => {
                      let s = o.value || o.text;
                      return wt(s);
                    })
                  : Array.from(n.target.selectedOptions).map(
                      (o) => o.value || o.text,
                    );
              {
                let o = n.target.value;
                return t.includes("number")
                  ? wt(o)
                  : t.includes("trim")
                  ? o.trim()
                  : o;
              }
            }
          })
      );
    }
    function wt(e) {
      let t = e ? parseFloat(e) : null;
      return ii(t) ? t : e;
    }
    function ni(e, t) {
      return e == t;
    }
    function ii(e) {
      return !Array.isArray(e) && !isNaN(e);
    }
    p("cloak", (e) =>
      queueMicrotask(() => h(() => e.removeAttribute(A("cloak")))),
    );
    tr(() => `[${A("init")}]`);
    p(
      "init",
      I((e, { expression: t }) =>
        typeof t == "string" ? !!t.trim() && v(e, t, {}, !1) : v(e, t, {}, !1),
      ),
    );
    p("text", (e, { expression: t }, { effect: r, evaluateLater: n }) => {
      let i = n(t);
      r(() => {
        i((o) => {
          h(() => {
            e.textContent = o;
          });
        });
      });
    });
    p("html", (e, { expression: t }, { effect: r, evaluateLater: n }) => {
      let i = n(t);
      r(() => {
        i((o) => {
          e.innerHTML = o;
        });
      });
    });
    Y(ye(":", xe(A("bind:"))));
    p(
      "bind",
      (
        e,
        { value: t, modifiers: r, expression: n, original: i },
        { effect: o },
      ) => {
        if (!t) return oi(e, n, i, o);
        if (t === "key") return si(e, n);
        let s = m(e, n);
        o(() =>
          s((a) => {
            a === void 0 && n.match(/\./) && (a = ""), h(() => ue(e, t, a, r));
          }),
        );
      },
    );
    function oi(e, t, r, n) {
      let i = m(e, t),
        o = [];
      n(() => {
        for (; o.length; ) o.pop()();
        i((s) => {
          let a = Object.entries(s).map(([l, u]) => ({ name: l, value: u }));
          a = a.filter(
            (l) =>
              !(
                typeof l.value == "object" &&
                !Array.isArray(l.value) &&
                l.value !== null
              ),
          );
          let c = qt(a);
          (a = a.map((l) =>
            c.find((u) => u.name === l.name)
              ? { name: `x-bind:${l.name}`, value: `"${l.value}"` }
              : l,
          )),
            re(e, a, r).map((l) => {
              o.push(l.runCleanups), l();
            });
        });
      });
    }
    function si(e, t) {
      e._x_keyExpression = t;
    }
    Ee(() => `[${A("data")}]`);
    p(
      "data",
      I((e, { expression: t }, { cleanup: r }) => {
        t = t === "" ? "{}" : t;
        let n = {};
        te(n, e);
        let i = {};
        pr(i, n);
        let o = v(e, t, { scope: i });
        o === void 0 && (o = {}), te(o, e);
        let s = w(o);
        he(s);
        let a = W(e, s);
        s.init && v(e, s.init),
          r(() => {
            a(), s.destroy && v(e, s.destroy);
          });
      }),
    );
    p("show", (e, { modifiers: t, expression: r }, { effect: n }) => {
      let i = m(e, r),
        o = () =>
          h(() => {
            (e.style.display = "none"), (e._x_isShown = !1);
          }),
        s = () =>
          h(() => {
            e.style.length === 1 && e.style.display === "none"
              ? e.removeAttribute("style")
              : e.style.removeProperty("display"),
              (e._x_isShown = !0);
          }),
        a = () => setTimeout(s),
        c = oe(
          (d) => (d ? s() : o()),
          (d) => {
            typeof e._x_toggleAndCascadeWithTransitions == "function"
              ? e._x_toggleAndCascadeWithTransitions(e, d, s, o)
              : d
              ? a()
              : o();
          },
        ),
        l,
        u = !0;
      n(() =>
        i((d) => {
          (!u && d === l) ||
            (t.includes("immediate") && (d ? a() : o()), c(d), (l = d), (u = !1));
        }),
      );
    });
    p("for", (e, { expression: t }, { effect: r, cleanup: n }) => {
      let i = ci(t),
        o = m(e, i.items),
        s = m(e, e._x_keyExpression || "index");
      (e._x_prevKeys = []),
        (e._x_lookup = {}),
        r(() => ai(e, i, o, s)),
        n(() => {
          Object.values(e._x_lookup).forEach((a) => a.remove()),
            delete e._x_prevKeys,
            delete e._x_lookup;
        });
    });
    function ai(e, t, r, n) {
      let i = (s) => typeof s == "object" && !Array.isArray(s),
        o = e;
      r((s) => {
        li(s) && s >= 0 && (s = Array.from(Array(s).keys(), (f) => f + 1)),
          s === void 0 && (s = []);
        let a = e._x_lookup,
          c = e._x_prevKeys,
          l = [],
          u = [];
        if (i(s))
          s = Object.entries(s).map(([f, _]) => {
            let x = Kr(t, _, f, s);
            n((R) => u.push(R), { scope: { index: f, ...x } }), l.push(x);
          });
        else
          for (let f = 0; f < s.length; f++) {
            let _ = Kr(t, s[f], f, s);
            n((x) => u.push(x), { scope: { index: f, ..._ } }), l.push(_);
          }
        let d = [],
          y = [],
          C = [],
          H = [];
        for (let f = 0; f < c.length; f++) {
          let _ = c[f];
          u.indexOf(_) === -1 && C.push(_);
        }
        c = c.filter((f) => !C.includes(f));
        let de = "template";
        for (let f = 0; f < u.length; f++) {
          let _ = u[f],
            x = c.indexOf(_);
          if (x === -1) c.splice(f, 0, _), d.push([de, f]);
          else if (x !== f) {
            let R = c.splice(f, 1)[0],
              k = c.splice(x - 1, 1)[0];
            c.splice(f, 0, k), c.splice(x, 0, R), y.push([R, k]);
          } else H.push(_);
          de = _;
        }
        for (let f = 0; f < C.length; f++) {
          let _ = C[f];
          a[_].remove(), (a[_] = null), delete a[_];
        }
        for (let f = 0; f < y.length; f++) {
          let [_, x] = y[f],
            R = a[_],
            k = a[x],
            q = document.createElement("div");
          h(() => {
            k.after(q), R.after(k), q.before(R), q.remove();
          }),
            Qe(k, l[u.indexOf(x)]);
        }
        for (let f = 0; f < d.length; f++) {
          let [_, x] = d[f],
            R = _ === "template" ? o : a[_],
            k = l[x],
            q = u[x],
            pe = document.importNode(o.content, !0).firstElementChild;
          W(pe, w(k), o),
            h(() => {
              R.after(pe), O(pe);
            }),
            typeof q == "object" &&
              we(
                "x-for key cannot be an object, it must be a string or an integer",
                o,
              ),
            (a[q] = pe);
        }
        for (let f = 0; f < H.length; f++) Qe(a[H[f]], l[u.indexOf(H[f])]);
        o._x_prevKeys = u;
      });
    }
    function ci(e) {
      let t = /,([^,\}\]]*)(?:,([^,\}\]]*))?$/,
        r = /^\s*\(|\)\s*$/g,
        n = /([\s\S]*?)\s+(?:in|of)\s+([\s\S]*)/,
        i = e.match(n);
      if (!i) return;
      let o = {};
      o.items = i[2].trim();
      let s = i[1].replace(r, "").trim(),
        a = s.match(t);
      return (
        a
          ? ((o.item = s.replace(t, "").trim()),
            (o.index = a[1].trim()),
            a[2] && (o.collection = a[2].trim()))
          : (o.item = s),
        o
      );
    }
    function Kr(e, t, r, n) {
      let i = {};
      return (
        /^\[.*\]$/.test(e.item) && Array.isArray(t)
          ? e.item
              .replace("[", "")
              .replace("]", "")
              .split(",")
              .map((s) => s.trim())
              .forEach((s, a) => {
                i[s] = t[a];
              })
          : /^\{.*\}$/.test(e.item) && !Array.isArray(t) && typeof t == "object"
          ? e.item
              .replace("{", "")
              .replace("}", "")
              .split(",")
              .map((s) => s.trim())
              .forEach((s) => {
                i[s] = t[s];
              })
          : (i[e.item] = t),
        e.index && (i[e.index] = r),
        e.collection && (i[e.collection] = n),
        i
      );
    }
    function li(e) {
      return !Array.isArray(e) && !isNaN(e);
    }
    function zr() {}
    zr.inline = (e, { expression: t }, { cleanup: r }) => {
      let n = P(e);
      n._x_refs || (n._x_refs = {}),
        (n._x_refs[t] = e),
        r(() => delete n._x_refs[t]);
    };
    p("ref", zr);
    p("if", (e, { expression: t }, { effect: r, cleanup: n }) => {
      let i = m(e, t),
        o = () => {
          if (e._x_currentIfEl) return e._x_currentIfEl;
          let a = e.content.cloneNode(!0).firstElementChild;
          return (
            W(a, {}, e),
            h(() => {
              e.after(a), O(a);
            }),
            (e._x_currentIfEl = a),
            (e._x_undoIf = () => {
              a.remove(), delete e._x_currentIfEl;
            }),
            a
          );
        },
        s = () => {
          !e._x_undoIf || (e._x_undoIf(), delete e._x_undoIf);
        };
      r(() =>
        i((a) => {
          a ? o() : s();
        }),
      ),
        n(() => e._x_undoIf && e._x_undoIf());
    });
    Y(ye("@", xe(A("on:"))));
    p(
      "on",
      I((e, { value: t, modifiers: r, expression: n }, { cleanup: i }) => {
        let o = n ? m(e, n) : () => {},
          s = fe(e, t, r, (a) => {
            o(() => {}, { scope: { $event: a }, params: [a] });
          });
        i(() => s());
      }),
    );
    S.setEvaluator(et);
    S.setReactivityEngine({ reactive: ke, effect: gr, release: yr, raw: g });
    var Et = S;
    window.Alpine = Et;
    queueMicrotask(() => {
      Et.start();
    });
  })();
  