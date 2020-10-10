# Switch State

Sometimes when developing you want to rapidly switch between different variations of a file / multiple files. This utility solves that problem.

Imagine the following file, "sample.c":

```c
//SEC new
//void new_func(void);
//ENDSEC

//SEC old
//void old_func(void);
//ENDSEC
```

`ss.py sample.c -s new` produces the following:

```c
//SEC new
void new_func(void);
//ENDSEC

//SEC old
//void old_func(void);
//ENDSEC
```

`ss.py sample.c -s old` produces the following:

```c
//SEC new
//void new_func(void);
//ENDSEC

//SEC old
void old_func(void);
//ENDSEC
```

`ss.py sample.c` (no `-s` means no state to activate) produces the following:

```c
//SEC new
//void new_func(void);
//ENDSEC

//SEC old
//void old_func(void);
//ENDSEC
```

Use `-c` to specify the comment character. By default, the program assumes c-style comments (`//`)

# TODO
- Support activating multiple file states at once
- Auto-detect the comment syntax in a file based upon its extension & have a fall-back option if the program can't auto-detect the comment syntax
