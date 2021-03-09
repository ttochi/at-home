# outposts
https://aws.amazon.com/ko/outposts/

이건 그냥 aws의 피지컬 환경을 회사에 설치해주겠다는 의미인거같은데?ㅋㅋ

# eks and iam

https://medium.com/swlh/cross-account-iam-roles-on-amazon-eks-d2922d77ab8f

# Terraform

인프라 요소들을 코드로 관리할 수 있도록 도와주는 도구래.
이거 써서 관리하면 대따 팬시하겠다


----

https://www.youtube.com/watch?v=O3znWPUdt18

# eks가 일반 k8s와는 다른 점?

우리가 알아야 할 것!
eks는 kubernetes cluster의 마스터 노드를 담당해주고 있다.
기본적으로 클러스터를 생성한 iam user가 k8s cluster master 역할을 갖게 됨.
기존 k8s와 다른 점은 kubectl 명령을 날릴 때,
- k8s api server 인증 토큰
- iam 인증 토큰
을 둘 다 날린다는 거

EKS 생성 시 k8s 클러스터에 `aws-auth`라는 config map이 추가되어있음
여기서 eks master node에 join한 worker node들에 대한 권한을 관리함
`kubectl edit configmap aws-auth -n kube-system`

즉, mlp는 EKS 환경을 구성해 (master node)
그리고 사용자 쪽에서 워커노드 생성을 위한 role을 만들어준다. (또는 워커노드까지 만들어야 할 수도 있음)
이 role 자체가 assumeRole이 되는 거지.. 그리고 이 롤에



> Fargate on EKS
https://www.youtube.com/watch?v=N0uLK5syctU

----

https://www.alcide.io/kubernetes-as-a-service-eks-vs.-aks-vs.-gke/
https://blog.nuricloud.com/aws-amazon-eks-intro-usages/
https://docs.aws.amazon.com/eks/latest/userguide/worker.html
https://docs.aws.amazon.com/eks/latest/userguide/update-managed-node-group.html
https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html
https://aws.amazon.com/ko/premiumsupport/knowledge-center/amazon-eks-cluster-access/
https://aws.amazon.com/ko/premiumsupport/knowledge-center/eks-worker-nodes-cluster/
https://aws.amazon.com/ko/blogs/containers/enabling-cross-account-access-to-amazon-eks-cluster-resources/
