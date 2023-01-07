# Tech Team Rota Generation

## Context

This project has been created since it has become a chore to generate the team rota for the Sunday services, it would be much easier of this could be generate by simply updating individual unavilability and then the code outputs the rota for a specific time period.

## Requirements for rota generation (in order of prioritisation)

- [x] Can specify dates for generation between certain time periods
- [x] Exports csv file of rota with dates and individuals working
- [x] No-one does the same role back to back
- [x] Can exclude dates specified by individuals
- [ ] Equal working shifts - equal number total (if one can only work certain shifts reduced shifts)
  - [x] Count 2 of every position, if someone has done a role more than twice they are required a break from that role until all others have reached 2 then all is reset. This only applies if the individual can do all roles
  - [x] Give breaks after 3 shifts back to back
- [ ] Extract dates for rota generation

### Nice to Haves

- [x] Move team members to a csv file
- [x] Have people that work only certain roles e.g. Person X only on camera duty
- [ ] Export as a pdf file
- [ ] Can exclude months for individual - if they go to uni
- [ ] Use of spare individual in case of emergency e.g. Person R emergency worker
- [ ] Configure special services if there are and assign additional role
- [ ] Generate positions based on number of equipment
- [ ] Use of probability to allocate members to shifts