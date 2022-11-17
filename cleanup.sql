/* The Whitespace solutions often also have the code in non-whitespace! Can't have that! */
DELETE FROM solutions
WHERE lang = "Whitespace" AND TRIM(code, CHAR(20)||CHAR(10)||CHAR(9)||' ') <> '';

/* C# and F# have a whole bunch of variations of their names, let's fix that... */
UPDATE solutions SET lang = 'C#' WHERE lang LIKE '%C#%';
UPDATE solutions SET lang = 'C#' WHERE lang = 'C Sharp' COLLATE NOCASE;
UPDATE solutions SET lang = 'C#' WHERE lang = 'C_Sharp' COLLATE NOCASE;
UPDATE solutions SET lang = 'F#' WHERE lang LIKE '%F#%';
UPDATE solutions SET lang = 'F#' WHERE lang = 'F Sharp' COLLATE NOCASE;
UPDATE solutions SET lang = 'F#' WHERE lang = 'F_Sharp' COLLATE NOCASE;

/* Some langs have a few different spellings */
UPDATE solutions SET lang = 'bash' WHERE lang = 'bash' COLLATE NOCASE;
UPDATE solutions SET lang = 'C++' WHERE lang LIKE '%C++%';
UPDATE solutions SET lang = 'Clojure' WHERE lang LIKE '%clojure%';
UPDATE solutions SET lang = 'dc' WHERE lang = 'dc' COLLATE NOCASE;
UPDATE solutions SET lang = 'gnuplot' WHERE lang = 'gnuplot' COLLATE NOCASE;
UPDATE solutions SET lang = 'Haskell' WHERE lang LIKE 'Haskell%';
UPDATE solutions SET lang = 'JavaScript' WHERE lang = 'JavaScript' COLLATE NOCASE;
UPDATE solutions SET lang = 'NewLISP' WHERE lang = 'NewLISP' COLLATE NOCASE;
UPDATE solutions SET lang = 'plainTeX' WHERE lang = 'plainTeX' COLLATE NOCASE;
UPDATE solutions SET lang = 'sed' WHERE lang = 'sed' COLLATE NOCASE;
UPDATE solutions SET lang = 'Snobol' WHERE lang = 'Snobol' COLLATE NOCASE;
UPDATE solutions SET lang = 'TypeScript' WHERE lang = 'TypeScript' COLLATE NOCASE;
UPDATE solutions SET lang = 'x86 Assembly' WHERE lang LIKE '%x86%';
UPDATE solutions SET lang = 'XSLT' WHERE lang LIKE 'XSLT%';
UPDATE solutions SET lang = 'Zig' WHERE lang = 'Zig' COLLATE NOCASE;



/* too many different SQLs */
UPDATE solutions SET lang = 'SQL' WHERE lang LIKE '%SQL%';

/* too many different ALGOLs */
UPDATE solutions SET lang = 'ALGOL' WHERE lang LIKE 'ALGOL%';

/* too many different BASICs */
DELETE FROM solutions
WHERE lang LIKE '%BASIC%' AND lang <> "BASIC" AND lang <> "TI-83 BASIC";

/* too many different assemblys */
DELETE FROM solutions
WHERE lang LIKE '%assembly%' AND lang <> "x86 Assembly" AND lang <> "WebAssembly";

/* get rid of the most obscure languages */
DELETE FROM solutions
WHERE lang IN (
	SELECT lang
	FROM solutions
	/* protect a few interesting languages with not many solutions */
	WHERE lang NOT IN (
		'Agda', 'Odin', 'Idris', 'Whitespace', 'Pony', 'Koka',
		'Rockstar', 'Chef', 'WebAssembly', 'Golfscript', 'Janet',
		'LaTeX', 'LLVM', 'LOLCODE', 'Elm', 'Beef', 'Futhark'
	)
	GROUP BY lang
	HAVING count(lang) < 40
);

/* too short solutions are no fun */
DELETE FROM solutions
WHERE LENGTH(code) < 15;
