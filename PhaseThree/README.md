# Nautilus E-Commerce Proof of Concept
Scenario 1: As Nautilus grows it’s considering expanding from the US into Europe, but they’re worried about latency and performance for their ecommerce site.  They decided that they needed to have a regional deployment of their ecommerce site so that customer data can still be within Europe (for data privacy requirements) but inventory tracking is global.  They need to change their database architecture to achieve this within their relational database systems.  Their inventory system could still be centrally located, however the customer-specific information data should live in-region. 

Your solution should:

* Focus on 1 of 2 Well-Architected Pillars (Security or Performance Efficiency).
* Contain a read/write inventory database that is accessible within 1 US and 1 EU region, and up to date at all times within 3-5 seconds.
* A region-specific customer information database.
* A sample POC website that when accessed by visitors, is able to route customers to the nearest region 

# Proposed Solution

<img width="1000" alt="NautilusArchDiagram" src="https://user-images.githubusercontent.com/61606335/185249536-119c0f6d-a9f8-44ba-ad23-207f1cd9a8d6.png">

