// B01 "The first tool is Clay."  724-790
ground("warm");
const K = buildTracker({});
const tC = T(738);
K.cards.forEach((c, i) => cardState(c, i === 0 ? [[0, 0], [0.02, 1, 0.5], [tC, 2, 0.8]] : [[0, 0], [0.1 + i * 0.07, 1, 0.55]]));
sweep(K.cards[0].c, tC + 0.5, 1.0);
A(K.rig, { s: [[0, 1.1], [DUR, 1.16, "lin"]], x: [[0, 40], [tC, 60], [tC + 1.0, 150, "expo"], [DUR, 170, "lin"]], ry: [[0, -9], [DUR, -5, "lin"]], rx: [[0, 6], [DUR, 5, "lin"]] });
el(stage, "vignette");
