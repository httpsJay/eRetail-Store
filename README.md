# eRetail-Store
Retail Stores operation management backend. (Proof Of Concept). Minimal Tech-Stack: Python, FLASK, LMDB


Requirements Conversation: 

1.  Users will use /api/submit to send json structured data using POST method and
    on the other side our Service will receive.

2.  Each job can take at most 1 hours of time also. So, We should think of
    multiple processing entities.

3. /api/submit : In the correct scenario, count will be equal to number of visits items.

4. Should we ignore creating jobs when count is not equal to the number of visits? (Return Error Response)

5.  Download and Process images

6. "After this the results are stored at an image level."
    - Image Level data collection

7.  csv data will be used as Store related Meta-Data for Dashboard

8. /api/status?jobid=  api will fetch information of the current status of a
    job.
