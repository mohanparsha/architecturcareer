Operating Systems Unit 1, version 3.3 (November 2026)

- Corrected the context-switch example. A 10 ms quantum gives about 100 switches a second on one CPU, not 5,000. The example now states its assumptions, shows the working for four quantum sizes, and adds how long each of 50 processes waits for its turn.
- Corrected the textbook chapter references against the table of contents of Operating System Concepts, 10th Edition (2018). Scheduling criteria and algorithms, the convoy effect and aging are in Chapter 5 (Sections 5.1 to 5.3), not Chapter 3, and the page now says so.
- Corrected "trap" and "exception". The textbook treats them as one mechanism with two causes (an error, or a system call), so the table, glossary, exam-trap card and practice question no longer teach them as two different things.
- Corrected the Round Robin example: every process gets its first CPU time by t=12, not t=16. All other worked scheduling figures were recomputed and are unchanged.
- Corrected the priority example: a short job running last in a finite batch is not starvation. Starvation means waiting indefinitely.
- Updated the Linux and Windows details: Linux is a monolithic kernel with loadable modules, it has been moving from the CFS scheduler to EEVDF since kernel 6.6, and WSL 2 runs a real Linux kernel in a virtual machine (only WSL 1 translated system calls).
- Corrected the size of saved CPU state (the x86-64 FXSAVE area alone is 512 bytes, not 100 to 200), moved mmap to the communications group of system calls to match the textbook, and noted that a TLB is not flushed on every switch when entries are tagged per process.
- Removed figures that had no source ("Linux: 95% C, 5% assembly", "thousands of switches per second") and the label "Master Edition".
- Added a line near the top saying what the page covers, that it is not tied to one university's syllabus, and that it is an independent study aid not affiliated with the textbook's authors or publisher.
- Added a Sources section with links to the textbook's table of contents and slides, Linux kernel documentation, Microsoft, Intel reference and Apple pages, plus links to the Network Concepts Guide and the Cybersecurity Career Roadmap.
- Improved phone and keyboard use: the navigation bar no longer covers the screen on a phone, diagrams keep their alignment, section links no longer hide the heading, quiz answers can be changed, and the back-to-top button no longer covers the footer.
- Added the shared site header and footer, the CC BY-NC-SA 4.0 licence, and British spelling throughout.
