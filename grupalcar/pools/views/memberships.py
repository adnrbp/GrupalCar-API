"""Pool membership views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Serializers
from grupalcar.pools.serializers import MembershipModelSerializer, AddMemberSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from grupalcar.pools.permissions.memberships import IsActivePoolMember, IsSelfMember

# Models
from grupalcar.pools.models import Pool, Membership, Invitation

class MembershipViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Pool membership view set."""

    serializer_class = MembershipModelSerializer

    def dispatch(self,request,*args,**kwargs):
        """Verify that the pool exists."""
        slug_name = kwargs['slug_name']
        self.pool = get_object_or_404(
            Pool,
            slug_name=slug_name
        )
        return super(MembershipViewSet,self).dispatch(request, *args, **kwargs)
        
    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action != 'create':
            permissions.append(IsActivePoolMember)
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
        return [permission() for permission in permissions]

    def get_queryset(self):
        """Return pool members."""
        return Membership.objects.filter(
            pool=self.pool,
            is_active=True
        )

    def get_object(self):
        """Return the pool member by using the user's username."""
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            pool=self.pool,
            is_active=True
        )

    def perform_destroy(self,instance):
        """Disable membership."""
        instance.is_active=False
        instance.save()

    @action(detail=True,methods=['get'])
    def invitations(self,request, *args, **kwargs):
        """Retrieve a member's used and unused invitations codes 

        Will return a list containing all the members that have
        used its invitations and another list containing the
        invitations that haven't being used yet.
        """
        member = self.get_object()
        invited_members = Membership.objects.filter(
            pool=self.pool,
            invited_by=request.user,
            is_active=True
        )

        unused_invitations = Invitation.objects.filter(
            pool=self.pool,
            issued_by=request.user,
            used=False
        ).values_list('code')

        # show sended invitations that were never used by invited user
        revocable_invitations = member.remaining_invitations - len(unused_invitations)

        recreated_invitations = [x[0] for x in unused_invitations]

        #create missing invitations
        for i in range(0,revocable_invitations):
            recreated_invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    pool=self.pool
                ).code
            )
        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
            'invitations': recreated_invitations
        }

        return Response(data)

    def create(self,request, *args, **kwargs):
        """Handle member creation from invitation code."""
        serializer = AddMemberSerializer(
            data=request.data,
            context={'pool': self.pool, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)