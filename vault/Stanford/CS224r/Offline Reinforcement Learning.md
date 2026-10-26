
Why offline RL?
- In online RL: we collect data, and update policy on the latest data or data so far
- Offline RL process: Given static dataset, train policy on provided dataset

When is offline RN useful?
- leverage datasets collected by people, existing systems
- Onlien policy collection may be risky, unsafe,
- reuse previously collected data rather than recollecting

Oftentimes its good to use a blend of offline and online RL:
- example: autonomous driving vehicles, often good to collected a month worth of data, perform offline RL with the newly collected data, and then deploy the new policy.

